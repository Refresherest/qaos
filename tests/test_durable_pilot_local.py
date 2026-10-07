"""Synthetic, local-only one-attempt pilot handoff tests (WO-178)."""

from __future__ import annotations

import copy
import json
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace

import pytest

from qaos.artifacts import ArtifactManager
from qaos.objectives import Objective
from qaos.planner import Task
from qaos.storage import create_stores
from qaos.workers.durable_pilot import (
    PILOT_RUNTIME_PINS, prepare_and_claim, revalidate_before_send,
)
from qaos.workers.pilot_admission import prepare_python_pilot


TOOLS = Path(__file__).parents[1] / "tools" / "qaos-worker"
sys.path.insert(0, str(TOOLS))
import qaos_worker_pilot as pilot


NOW = datetime(2026, 10, 4, 12, 0, tzinfo=timezone.utc)
SOURCE = 'def value():\n    return "SYNTHETIC_CANDIDATE_MARKER"\n'
ACCEPTANCE = 'assert True, "synthetic independent acceptance"\n'


def test_runtime_pins_match_reviewed_pilot_controller():
    assert dict(PILOT_RUNTIME_PINS) == pilot.PILOT_RUNTIME


class LocalClaimQueue:
    """Small in-memory contract fake; transaction proof belongs to queue tests."""

    def __init__(self, stores, *, fail_claim=False):
        self.lock = threading.Lock()
        self._stores = stores
        self.fail_claim = fail_claim
        self.claims = []
        self.status = None
        self.envelope = None
        self.unknown_calls = 0
        self.send_consumptions = 0
        self.release_capability = b"local-only-capability".ljust(32, b"0")

    def claim_pilot(self, queue_item_id, envelope):
        if self.fail_claim:
            raise RuntimeError("synthetic commit failure")
        self.claims.append(queue_item_id)
        self.envelope = copy.deepcopy(envelope)
        self.status = "pilot_claimed"
        return self.release_capability

    def get_pilot_claim(self, queue_item_id):
        with self.lock:
            if queue_item_id != "queue-1" or self.envelope is None:
                raise ValueError("no canonical claim")
            return {
                "status": self.status,
                "pilot_attempt": copy.deepcopy(self.envelope),
            }

    def mark_pilot_unknown(self, queue_item_id):
        assert queue_item_id == "queue-1"
        with self.lock:
            self.unknown_calls += 1
            self.status = "pilot_unknown"

    def consume_pilot_send_authority(self, queue_item_id, envelope, capability):
        with self.lock:
            if (queue_item_id != "queue-1" or self.status != "pilot_claimed"
                    or self.envelope != envelope
                    or capability != self.release_capability):
                raise ValueError("pilot release authority was already consumed")
            self.send_consumptions += 1
            self.status = "pilot_unknown"


@pytest.fixture
def admitted(tmp_path):
    objective = Objective("One synthetic Python pilot", objective_id="objective-1")
    task = Task("Create candidate", task_id="task-1")
    item = SimpleNamespace(
        objective=objective.goal,
        objective_id=objective.objective_id,
        task_id=task.task_id,
        action=task,
        queue_item_id="queue-1",
        status="pending",
        result=None,
    )
    stores = create_stores(tmp_path)
    ids = iter(("candidate-1", "acceptance-1"))
    artifacts = ArtifactManager(stores=stores, id_generator=lambda: next(ids))
    correlation = {"objective_id": objective.objective_id, "task_id": task.task_id}
    artifacts.create(
        "candidate", "python_candidate", "candidate-author", objective.goal,
        SOURCE, {**correlation, "pilot_role": "candidate"},
    )
    artifacts.create(
        "acceptance", "python_acceptance", "acceptance-author", objective.goal,
        ACCEPTANCE, {**correlation, "pilot_role": "acceptance"},
    )
    package = prepare_python_pilot(
        objective, task, item, artifacts, "candidate-1", "acceptance-1",
    )
    return package, artifacts, stores


def claim(admitted, queue=None):
    package, _artifacts, stores = admitted
    queue = queue or LocalClaimQueue(stores)
    claimed = prepare_and_claim(
        queue, package, request_builder=pilot.build_pilot_request, now=NOW,
    )
    return queue, claimed


def test_claim_commits_before_releasing_exact_wire_and_header_only_envelope(admitted):
    package, artifacts, stores = admitted
    queue, claimed = claim(admitted)
    assert queue.claims == ["queue-1"]
    assert queue.envelope == claimed.envelope
    assert set(claimed.envelope) == {
        "queue_item_id", "objective_id", "task_id", "candidate_artifact",
        "acceptance_artifact", "request", "request_sha256", "claimed_at",
    }
    encoded_claim = json.dumps(queue.envelope)
    assert "SYNTHETIC_CANDIDATE_MARKER" not in encoded_claim
    assert ACCEPTANCE not in encoded_claim
    assert claimed.request["members"] == package.manifest()
    before = stores.artifact_db.load()
    wire = revalidate_before_send(queue, claimed, now=NOW)
    assert isinstance(wire, bytes) and wire.startswith(pilot.encode_frame(
        pilot.canonical_json(claimed.request), pilot.REQUEST_LIMIT,
    ))
    assert not hasattr(claimed, "wire")
    assert stores.artifact_db.load() == before
    assert queue.status == "pilot_unknown"
    assert queue.send_consumptions == 1
    assert queue.unknown_calls == 0


def test_release_authority_is_single_use(admitted):
    queue, claimed = claim(admitted)
    assert isinstance(revalidate_before_send(queue, claimed, now=NOW), bytes)
    with pytest.raises(ValueError, match="exact unspent authority"):
        revalidate_before_send(queue, claimed, now=NOW)
    assert queue.send_consumptions == 1
    assert queue.status == "pilot_unknown"


def test_concurrent_release_returns_wire_to_at_most_one_caller(admitted):
    queue, claimed = claim(admitted)
    start = threading.Barrier(3)

    def attempt(_index):
        start.wait()
        try:
            return revalidate_before_send(queue, claimed, now=NOW)
        except ValueError:
            return None

    with ThreadPoolExecutor(max_workers=2) as pool:
        first = pool.submit(attempt, 1)
        second = pool.submit(attempt, 2)
        start.wait()
        results = [first.result(), second.result()]
    assert sum(isinstance(result, bytes) for result in results) == 1
    assert results.count(None) == 1
    assert queue.send_consumptions == 1
    assert queue.status == "pilot_unknown"


def test_failed_commit_never_returns_wire(admitted):
    queue = LocalClaimQueue(admitted[2], fail_claim=True)
    with pytest.raises(RuntimeError, match="commit failure"):
        prepare_and_claim(
            queue, admitted[0], request_builder=pilot.build_pilot_request, now=NOW,
        )
    assert queue.envelope is None


def test_injected_builder_wire_mismatch_refuses_claim(admitted):
    queue = LocalClaimQueue(admitted[2])

    def malformed(package, *, now):
        request, wire = pilot.build_pilot_request(package, now=now)
        return request, wire + b"trailing"

    with pytest.raises(ValueError, match="wire"):
        prepare_and_claim(queue, admitted[0], request_builder=malformed, now=NOW)
    assert queue.claims == []


@pytest.mark.parametrize("change", ["extra_field", "runtime", "nonce"])
def test_noncanonical_builder_header_cannot_create_durable_claim(admitted, change):
    queue = LocalClaimQueue(admitted[2])

    def malformed(package, *, now):
        request, _wire = pilot.build_pilot_request(package, now=now)
        if change == "extra_field":
            request["credential"] = "synthetic-forbidden-field"
        elif change == "runtime":
            request["runtime"]["policy_id"] = "unreviewed-policy"
        else:
            request["nonce"] = "too-short"
        wire = pilot.encode_frame(pilot.canonical_json(request), pilot.REQUEST_LIMIT)
        for member in package.members:
            wire += pilot.encode_frame(member.payload, pilot.MEMBER_LIMIT)
        return request, wire

    with pytest.raises(ValueError, match="fields|runtime|nonce"):
        prepare_and_claim(queue, admitted[0], request_builder=malformed, now=NOW)
    assert queue.claims == []


@pytest.mark.parametrize("drift", ["bytes", "provenance", "creator", "missing"])
def test_fresh_canonical_artifact_drift_consumes_claim_without_wire(admitted, drift):
    package, artifacts, stores = admitted
    queue, claimed = claim(admitted)
    rows = stores.artifact_db.load()
    if drift == "missing":
        rows = [row for row in rows if row["artifact_id"] != "candidate-1"]
    else:
        candidate = next(row for row in rows if row["artifact_id"] == "candidate-1")
        if drift == "bytes":
            import hashlib

            candidate["content"] += "# changed\n"
            candidate["content_sha256"] = hashlib.sha256(
                candidate["content"].encode("utf-8")
            ).hexdigest()
        elif drift == "provenance":
            candidate["provenance"]["review_tag"] = "changed"
        else:
            candidate["creator"] = "a-different-author"
    stores.artifact_db.save(rows)
    with pytest.raises(ValueError, match="operator review"):
        revalidate_before_send(queue, claimed, now=NOW)
    assert queue.status == "pilot_unknown"
    assert queue.unknown_calls == 1


def test_stale_artifact_copy_cannot_override_queue_workspace_at_release(admitted, tmp_path):
    package, _artifacts, canonical_stores = admitted
    queue, claimed = claim(admitted)
    copied_stores = create_stores(tmp_path / "stale-copy")
    copied_stores.artifact_db.save(canonical_stores.artifact_db.load())
    stale_manager = ArtifactManager(stores=copied_stores)
    assert stale_manager.get_by_id(package.candidate_artifact.artifact_id) is not None

    rows = canonical_stores.artifact_db.load()
    candidate = next(row for row in rows if row["artifact_id"] == "candidate-1")
    candidate["content"] += "# canonical drift\n"
    import hashlib

    candidate["content_sha256"] = hashlib.sha256(
        candidate["content"].encode("utf-8")
    ).hexdigest()
    canonical_stores.artifact_db.save(rows)

    # Release has no caller-supplied ArtifactManager; it must reread the
    # Artifact store selected by the queue, not the still-valid stale copy.
    with pytest.raises(ValueError, match="operator review"):
        revalidate_before_send(queue, claimed, now=NOW)
    assert queue.status == "pilot_unknown"
    assert queue.send_consumptions == 0


def test_claim_refuses_package_from_a_different_artifact_workspace(admitted, tmp_path):
    package, _artifacts, canonical_stores = admitted
    other_stores = create_stores(tmp_path / "other-workspace")
    queue = LocalClaimQueue(other_stores)
    with pytest.raises(ValueError, match="canonical Artifact is missing"):
        prepare_and_claim(
            queue, package, request_builder=pilot.build_pilot_request, now=NOW,
        )
    assert queue.claims == []


def test_expired_claim_is_held_and_never_rebuilt(admitted):
    queue, claimed = claim(admitted)
    with pytest.raises(ValueError, match="operator review"):
        revalidate_before_send(
            queue, claimed, now=NOW + timedelta(minutes=3),
        )
    assert queue.status == "pilot_unknown"
    assert queue.claims == ["queue-1"]


@pytest.mark.parametrize("status", ["pilot_unknown", "pilot_evidence_recorded"])
def test_nonclaimed_status_never_releases_wire_or_reopens_attempt(admitted, status):
    queue, claimed = claim(admitted)
    queue.status = status
    with pytest.raises(ValueError, match="exact unspent authority"):
        revalidate_before_send(queue, claimed, now=NOW)
    assert queue.status == status
    assert queue.unknown_calls == 0


def test_persisted_claim_tamper_and_local_wire_tamper_refuse_release(admitted):
    queue, claimed = claim(admitted)
    queue.envelope["request_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="exact unspent authority"):
        revalidate_before_send(queue, claimed, now=NOW)
    assert queue.unknown_calls == 0

    queue, claimed = claim(admitted)
    tampered = replace(claimed, request={**claimed.request, "nonce": "changed"})
    with pytest.raises(ValueError, match="operator review"):
        revalidate_before_send(queue, tampered, now=NOW)
    assert queue.status == "pilot_unknown"


def test_unidentified_origin_is_ineligible_even_with_valid_artifacts(admitted):
    package = admitted[0]
    package.origin_item.queue_item_id = None
    queue = LocalClaimQueue(admitted[2])
    with pytest.raises(ValueError, match="queue_item_id"):
        prepare_and_claim(
            queue, package, request_builder=pilot.build_pilot_request, now=NOW,
        )
    assert queue.claims == []
