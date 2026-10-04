#!/usr/bin/env python3
"""Local-only controller contract for the one-file Python worker pilot.

This module prepares a framed request and validates a supplied response. It
does not open a connection, run candidate code, or mutate/persist a QueueItem.
"""

from __future__ import annotations

import base64
import hashlib
import os
import uuid
from datetime import datetime, timedelta, timezone

from qaos.workers.pilot_admission import PILOT_FILE_LIMIT, PILOT_PATHS, PilotPackage
from qaos_worker_broker import IMAGE_DIGEST, PILOT_POLICY_ID
from qaos_worker_exchange import (
    MEMBER_LIMIT, PROTOCOL, REQUEST_LIMIT, VERSION, canonical_json, encode_frame,
    validate_request,
)
from qaos_worker_probe import parse_timestamp, timestamp, validate_response


# These are local review pins, not a live worker configuration or authority to
# install the launcher. The file digest is checked by tests against the source.
PILOT_LAUNCHER_SHA256 = "1b8e20cbc63999244862544f5c9933fb14cf9701d22b455bb753d4ebf4a81403"
PILOT_SPEC_SHA256 = "6aca4382c76e69fab92ec607eae303ae90bd408a11286a950228510a7d54d1a0"
PILOT_RUNTIME = {
    "launcher_sha256": PILOT_LAUNCHER_SHA256,
    "image_digest": IMAGE_DIGEST,
    "policy_id": PILOT_POLICY_ID,
}
PILOT_TEST_ID = "pilot.python-single.acceptance"
PROJECTION_LIMIT = 4096
_MEMBER_ORDER = (("acceptance", PILOT_PATHS["acceptance"]),
                 ("candidate", PILOT_PATHS["candidate"]))
_LIMIT_REASONS = {"deadline", "stdout_limit", "stderr_limit", "oom"}
_FAILURE_REASONS = {
    "policy_rejected": {"policy_refused", "replay_refused"},
    "runtime_failed": {"runtime_refused", "replay_storage_failed", "runtime_error"},
    "cleanup_failed": {"cleanup_failed"},
}


def _validate_package(package: PilotPackage) -> None:
    if not isinstance(package, PilotPackage) or len(package.members) != 2:
        raise ValueError("pilot requires one canonical two-member package")
    if package.candidate_artifact.artifact_id == package.acceptance_artifact.artifact_id:
        raise ValueError("pilot requires independent Artifact identities")
    for member, (role, path) in zip(package.members, _MEMBER_ORDER, strict=True):
        ref = getattr(package, f"{role}_artifact")
        if member.role != role or member.path != path:
            raise ValueError("pilot member role/path is not fixed")
        if not isinstance(member.payload, bytes) or not 0 < len(member.payload) <= PILOT_FILE_LIMIT:
            raise ValueError("pilot member bytes exceed fixed bounds")
        try:
            member.payload.decode("utf-8", "strict")
        except UnicodeDecodeError as error:
            raise ValueError("pilot member is not UTF-8") from error
        if (hashlib.sha256(member.payload).hexdigest() != member.sha256
                or ref.content_sha256 != member.sha256):
            raise ValueError("pilot Artifact/member digest does not match bytes")


def _correlate_request(request: dict, package: PilotPackage) -> None:
    _validate_package(package)
    validate_request(request, PILOT_RUNTIME, now=parse_timestamp(request["created_at"]))
    if (request["objective_id"] != package.objective_id
            or request["task_id"] != package.task_id
            or request["candidate_artifact"] != package.candidate_artifact.as_dict()
            or request["acceptance_artifact"] != package.acceptance_artifact.as_dict()
            or request["members"] != package.manifest()):
        raise ValueError("pilot request does not match canonical Artifacts and task")


def build_pilot_request(package: PilotPackage, *, now=None) -> tuple[dict, bytes]:
    """Return one canonical request and its bounded frames, without transport."""
    _validate_package(package)
    observed = now or datetime.now(timezone.utc)
    if not isinstance(observed, datetime) or observed.tzinfo is None:
        raise ValueError("pilot request time must be timezone-aware")
    created = observed.astimezone(timezone.utc).replace(microsecond=0)
    request = {
        "protocol": PROTOCOL, "version": VERSION,
        "request_id": str(uuid.uuid4()),
        "nonce": base64.urlsafe_b64encode(os.urandom(32)).decode("ascii").rstrip("="),
        "created_at": timestamp(created),
        "expires_at": timestamp(created + timedelta(minutes=2)),
        "objective_id": package.objective_id,
        "task_id": package.task_id,
        "candidate_artifact": package.candidate_artifact.as_dict(),
        "acceptance_artifact": package.acceptance_artifact.as_dict(),
        "members": package.manifest(),
        "runtime": dict(PILOT_RUNTIME),
    }
    _correlate_request(request, package)
    wire = encode_frame(canonical_json(request), REQUEST_LIMIT)
    for member in package.members:
        wire += encode_frame(member.payload, MEMBER_LIMIT)
    return request, wire


def _validate_origin(queue_item, package: PilotPackage) -> None:
    if (queue_item is not package.origin_item
            or getattr(queue_item, "objective_id", None) != package.objective_id
            or getattr(queue_item, "task_id", None) != package.task_id
            or getattr(getattr(queue_item, "action", None), "task_id", None) != package.task_id
            or getattr(queue_item, "status", None) != "pending"
            or getattr(queue_item, "result", None) is not None):
        raise ValueError("QueueItem is not the unattempted pilot origin")


def _validate_pilot_evidence(response: dict, request: dict) -> None:
    outcome = response["outcome"]
    resource = response["resource_evidence"]
    acceptance = response["acceptance_results"]
    cleanup = response["cleanup"]
    exit_code = response["exit_code"]
    reason = response["termination_reason"]
    if (resource["spec_sha256"] not in {None, PILOT_SPEC_SHA256}
            or resource["fixture"] not in {None, "python-single"}
            or (resource["spec_sha256"] is None) != (resource["fixture"] is None)):
        raise ValueError("pilot resource evidence does not match fixed fixture")
    if type(response["oom_killed"]) is not bool:
        raise ValueError("pilot OOM evidence is invalid")
    if exit_code is not None and type(exit_code) is not int:
        raise ValueError("pilot exit evidence is invalid")
    if not isinstance(reason, str):
        raise ValueError("pilot termination reason is invalid")
    truncated = [stream["truncated"] for stream in (response["stdout"], response["stderr"])]
    if truncated != ([True, True] if outcome == "limit_terminated" else [False, False]):
        raise ValueError("pilot output truncation does not match outcome")
    if outcome in {"completed", "candidate_failed", "limit_terminated"}:
        if (cleanup != {"staging_removed": True, "launcher_cleanup_reported": True}
                or resource != {"fixture": "python-single", "spec_sha256": PILOT_SPEC_SHA256}
                or exit_code is None):
            raise ValueError("pilot execution lacks exact resource or cleanup evidence")
    if outcome in {"completed", "candidate_failed"}:
        expected_status = "passed" if outcome == "completed" else "failed"
        if (len(acceptance) != 1
                or acceptance[0].get("test_id") != PILOT_TEST_ID
                or acceptance[0].get("status") != expected_status
                or type(acceptance[0].get("duration_ms")) is not int
                or not 0 <= acceptance[0]["duration_ms"] <= 90000
                or reason != "completion" or response["oom_killed"] is not False
                or (exit_code == 0) is not (outcome == "completed")):
            raise ValueError("pilot acceptance and outcome evidence disagree")
    else:
        if acceptance:
            raise ValueError("non-acceptance outcome cannot claim a test result")
        if outcome == "limit_terminated":
            if reason not in _LIMIT_REASONS or (reason == "oom") is not response["oom_killed"]:
                raise ValueError("pilot limit evidence is inconsistent")
        elif reason not in _FAILURE_REASONS.get(outcome, set()):
            raise ValueError("pilot refusal evidence is inconsistent")
        elif outcome == "cleanup_failed" and cleanup == {
            "staging_removed": True, "launcher_cleanup_reported": True
        }:
            raise ValueError("cleanup failure cannot claim complete cleanup")
    started = parse_timestamp(response["started_at"])
    completed = parse_timestamp(response["completed_at"])
    created = parse_timestamp(request["created_at"])
    if completed - created > timedelta(minutes=2) or started < created:
        raise ValueError("pilot response exceeds one bounded attempt")


def validate_pilot_response(raw: bytes, request: dict, package: PilotPackage,
                            queue_item) -> dict:
    """Return a bounded result projection; leave QueueItem persistence to caller."""
    _correlate_request(request, package)
    _validate_origin(queue_item, package)
    response = validate_response(
        raw, request, expected_runtime=PILOT_RUNTIME,
        expected_fixture="python-single", expected_test_id=PILOT_TEST_ID,
        expected_spec_sha256=PILOT_SPEC_SHA256,
    )
    _validate_pilot_evidence(response, request)
    projection = {
        "kind": "worker_validation", "version": VERSION,
        "objective_id": package.objective_id, "task_id": package.task_id,
        "candidate_artifact": package.candidate_artifact.as_dict(),
        "acceptance_artifact": package.acceptance_artifact.as_dict(),
        "request_id": request["request_id"],
        "worker_instance_id": response["worker_instance_id"],
        "runtime": {
            **PILOT_RUNTIME, "runtime_version": response["runtime_version"],
        },
        "started_at": response["started_at"],
        "completed_at": response["completed_at"],
        "outcome": response["outcome"],
        "exit_code": response["exit_code"],
        "oom_killed": response["oom_killed"],
        "termination_reason": response["termination_reason"],
        "stdout": {key: response["stdout"][key] for key in ("bytes", "sha256", "truncated")},
        "stderr": {key: response["stderr"][key] for key in ("bytes", "sha256", "truncated")},
        "resource_evidence": dict(response["resource_evidence"]),
        "acceptance_results": [dict(value) for value in response["acceptance_results"]],
        "cleanup": dict(response["cleanup"]),
        "response_sha256": response["response_sha256"],
        "requires_operator_review": response["outcome"] not in {"completed", "candidate_failed"},
    }
    if len(canonical_json(projection)) > PROJECTION_LIMIT:
        raise ValueError("pilot result projection exceeds fixed bound")
    return projection
