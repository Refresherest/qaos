"""Local-only one-attempt pilot preparation against canonical queue authority.

This module never opens a transport or accepts an offline response. A caller
may receive the framed request only after the queue has committed its claim.
The returned bytes still require a fresh, fail-closed artifact check before a
later, separately authorized transport could use them.
"""

from __future__ import annotations

import copy
import base64
import hashlib
import json
import re
import struct
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from types import MappingProxyType
from typing import Callable

from qaos.artifacts import ArtifactManager
from qaos.workers.pilot_admission import (
    PILOT_FILE_LIMIT,
    PILOT_PATHS,
    PilotPackage,
    _member,
)


_TIMESTAMP = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z\Z")
_REQUEST_LIMIT = 64 * 1024
_MEMBER_ORDER = (("acceptance", PILOT_PATHS["acceptance"]),
                 ("candidate", PILOT_PATHS["candidate"]))
_REQUEST_FIELDS = frozenset({
    "protocol", "version", "request_id", "nonce", "created_at", "expires_at",
    "objective_id", "task_id", "candidate_artifact", "acceptance_artifact",
    "members", "runtime",
})
PILOT_RUNTIME_PINS = MappingProxyType({
    "launcher_sha256": "1b8e20cbc63999244862544f5c9933fb14cf9701d22b455bb753d4ebf4a81403",
    "image_digest": "python@sha256:b64631e04e4920160c50fbe8d8df828f7f35f06f425cb44aa09bca53e708a35a",
    "policy_id": "qaos.python-single.v1",
})


@dataclass(frozen=True)
class ClaimedPilot:
    """In-memory handoff; the queue, not this object, owns attempt authority."""

    queue_item_id: str
    request: dict = field(repr=False)
    envelope: dict = field(repr=False)
    package: PilotPackage = field(repr=False)
    release_capability: bytes = field(repr=False)


def _canonical_json(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8", "strict")


def _frame(payload: bytes) -> bytes:
    return struct.pack(">Q", len(payload)) + payload


def _wire_from_request(request: dict, package: PilotPackage) -> bytes:
    return _frame(_canonical_json(request)) + b"".join(
        _frame(member.payload) for member in package.members
    )


def _utc_now(now: datetime | None) -> datetime:
    observed = now if now is not None else datetime.now(timezone.utc)
    if not isinstance(observed, datetime) or observed.tzinfo is None:
        raise ValueError("pilot time must be timezone-aware")
    return observed.astimezone(timezone.utc)


def _parse_timestamp(value: object) -> datetime:
    if not isinstance(value, str) or not _TIMESTAMP.fullmatch(value):
        raise ValueError("pilot request timestamp is invalid")
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=timezone.utc,
        )
    except ValueError as error:
        raise ValueError("pilot request timestamp is invalid") from error


def validate_frozen_request_schema(request: dict) -> bytes:
    """Validate the fixed, reviewed python-single header before durable claim.

    This restates the broker's wire contract at the controller authority
    boundary; tests pin it to the existing pilot controller constants.
    """
    if not isinstance(request, dict) or set(request) != _REQUEST_FIELDS:
        raise ValueError("pilot request fields are invalid")
    if (request["protocol"] != "qaos.worker.validation"
            or type(request["version"]) is not int or request["version"] != 1):
        raise ValueError("pilot request protocol or version is invalid")
    try:
        request_id = uuid.UUID(request["request_id"], version=4)
    except (ValueError, AttributeError, TypeError) as error:
        raise ValueError("pilot request_id is invalid") from error
    if str(request_id) != request["request_id"]:
        raise ValueError("pilot request_id must be lowercase UUIDv4")
    nonce = request["nonce"]
    if not isinstance(nonce, str):
        raise ValueError("pilot nonce is invalid")
    try:
        nonce_bytes = base64.urlsafe_b64decode(nonce + "==")
    except Exception as error:
        raise ValueError("pilot nonce is invalid") from error
    if len(nonce_bytes) != 32 or base64.urlsafe_b64encode(nonce_bytes).decode().rstrip("=") != nonce:
        raise ValueError("pilot nonce is invalid")
    created = _parse_timestamp(request["created_at"])
    expires = _parse_timestamp(request["expires_at"])
    if not created < expires <= created + timedelta(minutes=2):
        raise ValueError("pilot request expiry is invalid")
    for label in ("objective_id", "task_id"):
        value = request[label]
        if not isinstance(value, str) or not value or len(value.encode("utf-8")) > 256:
            raise ValueError(f"pilot {label} is invalid")
    for label in ("candidate_artifact", "acceptance_artifact"):
        ref = request[label]
        if not isinstance(ref, dict) or set(ref) != {"artifact_id", "content_sha256"}:
            raise ValueError(f"pilot {label} fields are invalid")
        if (not isinstance(ref["artifact_id"], str) or not ref["artifact_id"]
                or len(ref["artifact_id"].encode("utf-8")) > 256
                or not isinstance(ref["content_sha256"], str)
                or not re.fullmatch(r"[0-9a-f]{64}", ref["content_sha256"])):
            raise ValueError(f"pilot {label} identity is invalid")
    if request["candidate_artifact"]["artifact_id"] == request["acceptance_artifact"]["artifact_id"]:
        raise ValueError("pilot Artifacts must be distinct")
    if request["runtime"] != dict(PILOT_RUNTIME_PINS):
        raise ValueError("pilot runtime pins do not match the reviewed contract")
    members = request["members"]
    if not isinstance(members, list) or len(members) != 2:
        raise ValueError("pilot request requires two members")
    for member, (role, path) in zip(members, _MEMBER_ORDER, strict=True):
        if not isinstance(member, dict) or set(member) != {"role", "path", "size", "sha256"}:
            raise ValueError("pilot member fields are invalid")
        if (member["role"] != role or member["path"] != path
                or type(member["size"]) is not int
                or not 0 < member["size"] <= PILOT_FILE_LIMIT
                or not isinstance(member["sha256"], str)
                or not re.fullmatch(r"[0-9a-f]{64}", member["sha256"])):
            raise ValueError("pilot member is outside the fixed contract")
    if (members[0]["sha256"] != request["acceptance_artifact"]["content_sha256"]
            or members[1]["sha256"] != request["candidate_artifact"]["content_sha256"]):
        raise ValueError("pilot member and Artifact digest differ")
    header = _canonical_json(request)
    if not 0 < len(header) <= _REQUEST_LIMIT:
        raise ValueError("pilot request exceeds fixed bounds")
    return header


def _assert_package(package: PilotPackage, *, require_pending: bool = True) -> str:
    if (not isinstance(package, PilotPackage)
            or len(package.members) != 2 or len(package.sources) != 2):
        raise ValueError("pilot requires one canonical two-member package")
    origin = package.origin_item
    queue_item_id = getattr(origin, "queue_item_id", None)
    if not isinstance(queue_item_id, str) or not queue_item_id:
        raise ValueError("pilot origin requires a canonical queue_item_id")
    if (getattr(origin, "objective_id", None) != package.objective_id
            or getattr(origin, "task_id", None) != package.task_id
            or getattr(getattr(origin, "action", None), "task_id", None) != package.task_id):
        raise ValueError("pilot origin does not correlate to canonical Objective/Task")
    if require_pending and (
        getattr(origin, "status", None) != "pending"
        or getattr(origin, "result", None) is not None
    ):
        raise ValueError("pilot origin is not an unattempted canonical QueueItem")
    if package.candidate_artifact.artifact_id == package.acceptance_artifact.artifact_id:
        raise ValueError("pilot requires distinct Artifact identities")
    creators = []
    for (member, source), (role, path) in zip(
        zip(package.members, package.sources, strict=True), _MEMBER_ORDER, strict=True,
    ):
        ref = getattr(package, f"{role}_artifact")
        if (member.role != role or member.path != path
                or source.artifact_id != ref.artifact_id
                or source.content_sha256 != ref.content_sha256
                or source.artifact_type != f"python_{role}"
                or source.objective != origin.objective
                or dict(source.provenance).get("objective_id") != package.objective_id
                or dict(source.provenance).get("task_id") != package.task_id
                or dict(source.provenance).get("pilot_role") != role):
            raise ValueError("pilot source identity or provenance has changed")
        if (not isinstance(member.payload, bytes)
                or not 0 < len(member.payload) <= PILOT_FILE_LIMIT
                or hashlib.sha256(member.payload).hexdigest() != member.sha256
                or member.sha256 != ref.content_sha256):
            raise ValueError("pilot member does not match canonical Artifact bytes")
        try:
            member.payload.decode("utf-8", "strict")
        except UnicodeDecodeError as error:
            raise ValueError("pilot member is not UTF-8") from error
        creators.append(source.creator)
    if creators[0] == creators[1]:
        raise ValueError("pilot candidate and acceptance require distinct creators")
    return queue_item_id


def _assert_request_and_wire(request: dict, wire: bytes, package: PilotPackage) -> bytes:
    if not isinstance(request, dict) or not isinstance(wire, bytes):
        raise ValueError("pilot builder must return a request and framed bytes")
    header = validate_frozen_request_schema(request)
    if (request.get("objective_id") != package.objective_id
            or request.get("task_id") != package.task_id
            or request.get("candidate_artifact") != package.candidate_artifact.as_dict()
            or request.get("acceptance_artifact") != package.acceptance_artifact.as_dict()
            or request.get("members") != package.manifest()):
        raise ValueError("pilot request does not match canonical package")
    expected = _wire_from_request(request, package)
    if wire != expected:
        raise ValueError("pilot wire does not match frozen request and Artifact bytes")
    created = _parse_timestamp(request.get("created_at"))
    expires = _parse_timestamp(request.get("expires_at"))
    if not created < expires <= created + timedelta(minutes=2):
        raise ValueError("pilot request expiry is invalid")
    return header


def prepare_and_claim(
    queue,
    package: PilotPackage,
    *,
    request_builder: Callable,
    now: datetime | None = None,
) -> ClaimedPilot:
    """Build once and durably claim before making any wire bytes available.

    ``request_builder`` must be the existing pure local ``build_pilot_request``
    contract. There is deliberately no transport argument or dispatch call.
    """
    observed = _utc_now(now)
    queue_item_id = _assert_package(package)
    _assert_fresh_artifacts(queue, package)
    request, wire = request_builder(package, now=observed)
    header = _assert_request_and_wire(request, wire, package)
    if not _parse_timestamp(request["created_at"]) <= observed < _parse_timestamp(request["expires_at"]):
        raise ValueError("pilot request is not currently valid")
    frozen_request = copy.deepcopy(request)
    envelope = {
        "queue_item_id": queue_item_id,
        "objective_id": package.objective_id,
        "task_id": package.task_id,
        "candidate_artifact": package.candidate_artifact.as_dict(),
        "acceptance_artifact": package.acceptance_artifact.as_dict(),
        "request": frozen_request,
        "request_sha256": hashlib.sha256(header).hexdigest(),
        "claimed_at": observed.replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    }
    # A failed or ambiguous commit never returns the framed request to a caller.
    release_capability = queue.claim_pilot(queue_item_id, copy.deepcopy(envelope))
    if not isinstance(release_capability, bytes) or len(release_capability) != 32:
        raise ValueError("pilot claim did not return a volatile release capability")
    # Do not expose framed bytes in the handoff object. The only public byte
    # release is the one-use, post-revalidation consume gate below.
    return ClaimedPilot(
        queue_item_id, frozen_request, envelope, package, release_capability,
    )


def _assert_fresh_artifacts(queue, package: PilotPackage) -> None:
    # The queue's selected workspace determines the canonical Artifact store.
    # A caller-supplied manager may point to a stale copy, even after reload().
    stores = getattr(queue, "_stores", None)
    if stores is None or getattr(stores, "artifact_db", None) is None:
        raise ValueError("pilot queue has no canonical Artifact store")
    artifacts = ArtifactManager(stores=stores)
    for source, original_member, (role, _path) in zip(
        package.sources, package.members, _MEMBER_ORDER, strict=True,
    ):
        artifact = artifacts.get_by_id(source.artifact_id)
        if artifact is None:
            raise ValueError(f"{role} canonical Artifact is missing")
        current_ref, current_member, current_source = _member(
            artifact, role, package.objective_id, package.task_id, source.objective,
        )
        if (current_ref != getattr(package, f"{role}_artifact")
                or current_source != source
                or current_member.manifest() != original_member.manifest()
                or current_member.payload != original_member.payload):
            raise ValueError(f"{role} canonical Artifact drifted after pilot claim")


def revalidate_before_send(
    queue,
    claimed: ClaimedPilot,
    *,
    now: datetime | None = None,
) -> bytes:
    """Return the original wire only for one still-claimed, unchanged attempt.

    Drift or expiry consumes the claim via ``pilot_unknown``. A successful
    validation also atomically consumes release authority before returning
    bytes, leaving the queue in the conservative unknown/held state. The
    method does not transmit bytes, and a restarted process cannot reconstruct
    this wire from the durable claim (which intentionally contains no source
    bytes).
    """
    observed = _utc_now(now)
    if not isinstance(claimed, ClaimedPilot):
        raise ValueError("pilot handoff must be a claimed in-memory request")
    persisted = queue.get_pilot_claim(claimed.queue_item_id)
    if (persisted.get("status") != "pilot_claimed"
            or persisted.get("pilot_attempt") != claimed.envelope):
        raise ValueError("pilot claim is no longer the exact unspent authority")
    try:
        if _assert_package(claimed.package, require_pending=False) != claimed.queue_item_id:
            raise ValueError("pilot queue identity changed")
        wire = _wire_from_request(claimed.request, claimed.package)
        header = _assert_request_and_wire(claimed.request, wire, claimed.package)
        if (claimed.envelope.get("request") != claimed.request
                or claimed.envelope.get("request_sha256") != hashlib.sha256(header).hexdigest()):
            raise ValueError("pilot request changed after durable claim")
        if observed >= _parse_timestamp(claimed.request["expires_at"]):
            raise ValueError("pilot request expired before send")
        _assert_fresh_artifacts(queue, claimed.package)
    except Exception as error:
        queue.mark_pilot_unknown(claimed.queue_item_id)
        raise ValueError("pilot claim consumed without send; operator review required") from error
    # Another caller may have passed the read check concurrently. Only the
    # canonical queue's atomic claimed -> unknown transition can grant release.
    queue.consume_pilot_send_authority(
        claimed.queue_item_id, claimed.envelope, claimed.release_capability,
    )
    return wire
