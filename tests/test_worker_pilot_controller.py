"""Controller contract tests for the local-only Python pilot (WO-174)."""

from __future__ import annotations

import hashlib
import io
import json
import sys
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path

import pytest

from qaos.artifacts import ArtifactManager
from qaos.objectives import Objective
from qaos.planner import Task
from qaos.queue import QueueItem
from qaos.storage import create_stores
from qaos.workers.pilot_admission import prepare_python_pilot


TOOLS = Path(__file__).parents[1] / "tools" / "qaos-worker"
sys.path.insert(0, str(TOOLS))
import qaos_worker_pilot as pilot
import qaos_worker_pilot_launcher as launcher
from qaos_worker_broker import RESPONSE_LIMIT
from qaos_worker_exchange import canonical_json, decode_request, encode_frame


NOW = datetime(2026, 9, 6, 12, 0, tzinfo=timezone.utc)
CANDIDATE_SOURCE = 'def value():\n    return "PILOT_PRIVATE_MARKER_8473"\n'
ACCEPTANCE_SOURCE = 'assert True, "independent check"\n'


def test_review_pins_match_separate_pilot_launcher():
    path = TOOLS / "qaos_worker_pilot_launcher.py"
    assert hashlib.sha256(path.read_bytes()).hexdigest() == pilot.PILOT_LAUNCHER_SHA256
    assert launcher.PILOT_SPEC_SHA256 == pilot.PILOT_SPEC_SHA256


@pytest.fixture
def prepared(tmp_path):
    objective = Objective("One Python pilot", objective_id="objective-1")
    task = Task("Make one Python file", task_id="task-1")
    queue_item = QueueItem(objective, "worker", action=task)
    identities = iter(("candidate-1", "acceptance-1"))
    artifacts = ArtifactManager(
        stores=create_stores(tmp_path), id_generator=lambda: next(identities)
    )
    correlation = {"objective_id": objective.objective_id, "task_id": task.task_id}
    artifacts.create(
        "candidate", "python_candidate", "candidate-author", objective.goal,
        CANDIDATE_SOURCE, {**correlation, "pilot_role": "candidate"},
    )
    artifacts.create(
        "acceptance", "python_acceptance", "acceptance-author", objective.goal,
        ACCEPTANCE_SOURCE, {**correlation, "pilot_role": "acceptance"},
    )
    package = prepare_python_pilot(
        objective, task, queue_item, artifacts, "candidate-1", "acceptance-1"
    )
    return package, queue_item


def framed_response(request, *, changes=None, corrupt_digest=False):
    """Produce one correlated fake broker frame, without executing any code."""
    empty = hashlib.sha256(b"").hexdigest()
    value = {
        "protocol": request["protocol"],
        "version": request["version"],
        "request_id": request["request_id"],
        "nonce": request["nonce"],
        "objective_id": request["objective_id"],
        "task_id": request["task_id"],
        "candidate_artifact": request["candidate_artifact"],
        "acceptance_artifact": request["acceptance_artifact"],
        "worker_instance_id": "qaos-worker",
        "launcher_sha256": pilot.PILOT_RUNTIME["launcher_sha256"],
        "runtime_version": "gvisor-20260831.0",
        "image_digest": pilot.PILOT_RUNTIME["image_digest"],
        "policy_id": pilot.PILOT_RUNTIME["policy_id"],
        "started_at": request["created_at"],
        "completed_at": request["created_at"],
        "outcome": "completed",
        "exit_code": 0,
        "oom_killed": False,
        "termination_reason": "completion",
        "stdout": {
            "bytes": 0, "sha256": empty, "truncated": False, "text_preview": "",
        },
        "stderr": {
            "bytes": 0, "sha256": empty, "truncated": False, "text_preview": "",
        },
        "resource_evidence": {
            "fixture": "python-single", "spec_sha256": pilot.PILOT_SPEC_SHA256,
        },
        "acceptance_results": [{
            "test_id": "pilot.python-single.acceptance",
            "status": "passed", "duration_ms": 7,
        }],
        "cleanup": {"staging_removed": True, "launcher_cleanup_reported": True},
    }
    value.update(changes or {})
    value["response_sha256"] = hashlib.sha256(canonical_json(value)).hexdigest()
    if corrupt_digest:
        value["response_sha256"] = "0" * 64
    return encode_frame(canonical_json(value), RESPONSE_LIMIT)


def test_build_request_is_fresh_canonical_and_exactly_matches_artifacts(prepared):
    package, queue_item = prepared
    request, wire = pilot.build_pilot_request(package, now=NOW)
    decoded, payloads = decode_request(io.BytesIO(wire), pilot.PILOT_RUNTIME, NOW)
    assert decoded == request
    assert request["runtime"] == pilot.PILOT_RUNTIME
    assert request["members"] == package.manifest()
    assert request["candidate_artifact"] == package.candidate_artifact.as_dict()
    assert request["acceptance_artifact"] == package.acceptance_artifact.as_dict()
    assert payloads == (
        ACCEPTANCE_SOURCE.encode("utf-8"), CANDIDATE_SOURCE.encode("utf-8")
    )
    assert request["objective_id"] == package.objective_id
    assert request["task_id"] == package.task_id
    second, second_wire = pilot.build_pilot_request(package, now=NOW)
    assert second["request_id"] != request["request_id"]
    assert second["nonce"] != request["nonce"]
    assert second_wire != wire
    assert queue_item.status == "pending" and queue_item.result is None


@pytest.mark.parametrize(
    "change",
    [
        lambda p: replace(p, members=(replace(p.members[0], payload=b"tampered"), p.members[1])),
        lambda p: replace(p, members=(replace(p.members[0], sha256="0" * 64), p.members[1])),
        lambda p: replace(p, members=(replace(p.members[0], path="acceptance/other.py"), p.members[1])),
        lambda p: replace(p, members=(replace(p.members[0], role="candidate"), p.members[1])),
        lambda p: replace(p, members=(p.members[0],)),
        lambda p: replace(p, members=(p.members[1], p.members[0])),
        lambda p: replace(p, candidate_artifact=replace(p.candidate_artifact, content_sha256="0" * 64)),
        lambda p: replace(p, acceptance_artifact=replace(p.acceptance_artifact, artifact_id=p.candidate_artifact.artifact_id)),
        lambda p: replace(p, objective_id=""),
        lambda p: replace(p, task_id=""),
    ],
)
def test_mutated_admission_package_fails_before_framing(prepared, change):
    package, _ = prepared
    with pytest.raises(ValueError):
        pilot.build_pilot_request(change(package), now=NOW)


def test_valid_response_returns_bounded_projection_without_mutating_queue(prepared):
    package, queue_item = prepared
    request, _ = pilot.build_pilot_request(package, now=NOW)
    projection = pilot.validate_pilot_response(
        framed_response(request), request, package, queue_item
    )
    assert isinstance(projection, dict)
    assert projection["outcome"] == "completed"
    assert CANDIDATE_SOURCE not in json.dumps(projection, ensure_ascii=False)
    assert "PILOT_PRIVATE_MARKER_8473" not in json.dumps(projection, ensure_ascii=False)
    assert "nonce" not in projection
    assert "text_preview" not in projection["stdout"]
    assert len(canonical_json(projection)) <= pilot.PROJECTION_LIMIT
    assert queue_item.status == "pending" and queue_item.result is None


@pytest.mark.parametrize(
    "change",
    [
        {"request_id": "different-request"},
        {"nonce": "different-nonce"},
        {"objective_id": "different-objective"},
        {"task_id": "different-task"},
        {"candidate_artifact": {"artifact_id": "other", "content_sha256": "0" * 64}},
        {"acceptance_artifact": {"artifact_id": "other", "content_sha256": "0" * 64}},
        {"worker_instance_id": "unknown-worker"},
        {"runtime_version": "unknown-runtime"},
        {"launcher_sha256": "0" * 64},
        {"image_digest": "other-image"},
        {"policy_id": "other-policy"},
        {"started_at": "2026-09-06T11:59:59Z"},
        {"completed_at": "2026-09-06T11:59:59Z"},
        {"exit_code": 7},
        {"oom_killed": True},
        {"termination_reason": "deadline"},
        {"cleanup": {"staging_removed": False, "launcher_cleanup_reported": True}},
        {"resource_evidence": {"fixture": "harmless", "spec_sha256": "0" * 64}},
        {"resource_evidence": {"fixture": "python-single", "spec_sha256": "0" * 64}},
        {"acceptance_results": []},
        {"acceptance_results": [{"test_id": "pilot.python-single.acceptance", "status": "failed", "duration_ms": 7}]},
    ],
)
def test_success_response_rejects_forged_semantics_without_queue_mutation(
    prepared, change
):
    package, queue_item = prepared
    request, _ = pilot.build_pilot_request(package, now=NOW)
    with pytest.raises(ValueError):
        pilot.validate_pilot_response(
            framed_response(request, changes=change), request, package, queue_item
        )
    assert queue_item.status == "pending" and queue_item.result is None


def test_response_digest_trailing_bytes_and_oversize_preview_are_rejected(prepared):
    package, queue_item = prepared
    request, _ = pilot.build_pilot_request(package, now=NOW)
    good = framed_response(request)
    malformed = [
        framed_response(request, corrupt_digest=True),
        good + b"trailing",
        framed_response(request, changes={"stdout": {
            "bytes": 481, "sha256": hashlib.sha256(b"x" * 481).hexdigest(),
            "truncated": False, "text_preview": "x" * 481,
        }}),
    ]
    for raw in malformed:
        with pytest.raises(ValueError):
            pilot.validate_pilot_response(raw, request, package, queue_item)
        assert queue_item.status == "pending" and queue_item.result is None


@pytest.mark.parametrize(
    "change",
    [
        lambda q: setattr(q, "objective_id", "other"),
        lambda q: setattr(q, "task_id", "other"),
        lambda q: setattr(q, "action", Task("other", task_id="other")),
        lambda q: setattr(q, "status", "running"),
        lambda q: setattr(q, "status", "completed"),
        lambda q: setattr(q, "result", {"already": "attempted"}),
    ],
)
def test_past_or_uncorrelated_queue_item_refuses_projection(prepared, change):
    package, queue_item = prepared
    request, _ = pilot.build_pilot_request(package, now=NOW)
    change(queue_item)
    with pytest.raises(ValueError):
        pilot.validate_pilot_response(
            framed_response(request), request, package, queue_item
        )


def test_same_ids_on_a_different_queue_item_do_not_claim_the_origin(prepared):
    package, queue_item = prepared
    request, _ = pilot.build_pilot_request(package, now=NOW)
    other = QueueItem(
        queue_item.objective, "worker",
        action=Task("same ID, different Task", task_id=package.task_id),
        objective_id=package.objective_id,
    )
    assert other.objective_id == queue_item.objective_id
    assert other.task_id == queue_item.task_id
    assert other.status == "pending" and other.result is None
    with pytest.raises(ValueError):
        pilot.validate_pilot_response(framed_response(request), request, package, other)


def test_candidate_failure_is_projected_as_failure_evidence(prepared):
    package, queue_item = prepared
    request, _ = pilot.build_pilot_request(package, now=NOW)
    frame = framed_response(request, changes={
        "outcome": "candidate_failed",
        "exit_code": 1,
        "acceptance_results": [{
            "test_id": "pilot.python-single.acceptance",
            "status": "failed", "duration_ms": 7,
        }],
    })
    projection = pilot.validate_pilot_response(frame, request, package, queue_item)
    assert projection["outcome"] == "candidate_failed"
    assert queue_item.status == "pending" and queue_item.result is None


def test_policy_refusal_remains_bounded_failure_evidence(prepared):
    package, queue_item = prepared
    request, _ = pilot.build_pilot_request(package, now=NOW)
    frame = framed_response(request, changes={
        "outcome": "policy_rejected", "exit_code": None,
        "termination_reason": "replay_refused", "acceptance_results": [],
        "resource_evidence": {"fixture": None, "spec_sha256": None},
        "cleanup": {"staging_removed": True, "launcher_cleanup_reported": False},
    })
    projection = pilot.validate_pilot_response(frame, request, package, queue_item)
    assert projection["outcome"] == "policy_rejected"
    assert CANDIDATE_SOURCE not in json.dumps(projection, ensure_ascii=False)
    assert queue_item.status == "pending" and queue_item.result is None


@pytest.mark.parametrize("outcome,reason,exit_code", [
    ("limit_terminated", "deadline", 137),
    ("runtime_failed", "runtime_error", 125),
])
def test_nonacceptance_execution_requires_operator_review(
    prepared, outcome, reason, exit_code
):
    package, queue_item = prepared
    request, _ = pilot.build_pilot_request(package, now=NOW)
    truncated = outcome == "limit_terminated"
    empty_stream = {
        "bytes": 0, "sha256": hashlib.sha256(b"").hexdigest(),
        "truncated": truncated, "text_preview": "",
    }
    frame = framed_response(request, changes={
        "outcome": outcome, "termination_reason": reason, "exit_code": exit_code,
        "acceptance_results": [], "stdout": empty_stream, "stderr": empty_stream,
    })
    projection = pilot.validate_pilot_response(frame, request, package, queue_item)
    assert projection["outcome"] == outcome
    assert projection["requires_operator_review"] is True
    assert projection["stdout"]["truncated"] is truncated
    assert queue_item.result is None


def test_limit_rejects_false_complete_stream_claim(prepared):
    package, queue_item = prepared
    request, _ = pilot.build_pilot_request(package, now=NOW)
    frame = framed_response(request, changes={
        "outcome": "limit_terminated", "termination_reason": "stdout_limit",
        "exit_code": 137, "acceptance_results": [],
    })
    with pytest.raises(ValueError, match="truncation"):
        pilot.validate_pilot_response(frame, request, package, queue_item)
