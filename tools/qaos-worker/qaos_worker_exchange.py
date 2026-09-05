#!/usr/bin/env python3
"""Strict framing and request validation for the QAOS worker exchange."""

from __future__ import annotations

import base64
import hashlib
import json
import re
import struct
import uuid
from datetime import datetime, timezone

PROTOCOL = "qaos.worker.validation"
VERSION = 1
REQUEST_LIMIT = 64 * 1024
MEMBER_LIMIT = 1024 * 1024
TOTAL_LIMIT = 8 * 1024 * 1024
MEMBER_COUNT_LIMIT = 32
PATH_RE = re.compile(r"[A-Za-z0-9._/-]{1,128}\Z")
SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")
REQUEST_FIELDS = {
    "protocol", "version", "request_id", "nonce", "created_at", "expires_at",
    "objective_id", "task_id", "candidate_artifact", "acceptance_artifact",
    "members", "runtime",
}
ARTIFACT_FIELDS = {"artifact_id", "content_sha256"}
MEMBER_FIELDS = {"role", "path", "size", "sha256"}
RUNTIME_FIELDS = {"launcher_sha256", "image_digest", "policy_id"}


class ProtocolError(ValueError):
    pass


def canonical_json(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def _object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ProtocolError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def decode_canonical_json(payload: bytes) -> dict:
    def reject_constant(value):
        raise ProtocolError(f"invalid JSON constant: {value}")
    try:
        text = payload.decode("utf-8", "strict")
        value = json.loads(
            text, object_pairs_hook=_object, parse_constant=reject_constant
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ProtocolError("invalid UTF-8 JSON") from error
    if not isinstance(value, dict):
        raise ProtocolError("JSON frame must be an object")
    try:
        canonical = canonical_json(value)
    except UnicodeEncodeError as error:
        raise ProtocolError("invalid Unicode JSON value") from error
    if canonical != payload:
        raise ProtocolError("JSON frame is not canonical")
    return value


def encode_frame(payload: bytes, limit: int) -> bytes:
    if len(payload) > limit:
        raise ProtocolError("frame exceeds limit")
    return struct.pack(">Q", len(payload)) + payload


def read_frame(stream, limit: int) -> bytes:
    header = _read_exact(stream, 8)
    if header is None:
        raise ProtocolError("premature frame header EOF")
    length = struct.unpack(">Q", header)[0]
    if length > limit:
        raise ProtocolError("frame exceeds limit")
    payload = _read_exact(stream, length)
    if payload is None:
        raise ProtocolError("premature frame payload EOF")
    return payload


def _read_exact(stream, length):
    chunks = []
    remaining = length
    while remaining:
        chunk = stream.read(remaining)
        if not chunk:
            return None
        chunks.append(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)


def _exact(value, fields, label):
    if not isinstance(value, dict) or set(value) != fields:
        raise ProtocolError(f"invalid {label} fields")


def _identity(value, label):
    if not isinstance(value, str) or not value or len(value.encode()) > 256:
        raise ProtocolError(f"invalid {label}")


def _timestamp(value, label):
    if not isinstance(value, str) or not value.endswith("Z"):
        raise ProtocolError(f"invalid {label}")
    try:
        parsed = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=timezone.utc
        )
    except ValueError as error:
        raise ProtocolError(f"invalid {label}") from error
    return parsed


def validate_request(request: dict, expected_runtime: dict, now=None) -> tuple[dict, ...]:
    _exact(request, REQUEST_FIELDS, "request")
    if request["protocol"] != PROTOCOL or request["version"] != VERSION:
        raise ProtocolError("unsupported protocol")
    try:
        parsed_id = uuid.UUID(request["request_id"], version=4)
    except (ValueError, AttributeError) as error:
        raise ProtocolError("invalid request_id") from error
    if str(parsed_id) != request["request_id"]:
        raise ProtocolError("request_id must be lowercase UUIDv4")
    try:
        nonce = base64.urlsafe_b64decode(request["nonce"] + "==")
    except Exception as error:
        raise ProtocolError("invalid nonce") from error
    if len(nonce) != 32 or base64.urlsafe_b64encode(nonce).decode().rstrip("=") != request["nonce"]:
        raise ProtocolError("invalid nonce")
    created = _timestamp(request["created_at"], "created_at")
    expires = _timestamp(request["expires_at"], "expires_at")
    observed = now or datetime.now(timezone.utc)
    if not (created <= observed <= expires and created < expires):
        raise ProtocolError("request is outside its validity window")
    if (expires - created).total_seconds() > 300:
        raise ProtocolError("request validity exceeds five minutes")
    _identity(request["objective_id"], "objective_id")
    _identity(request["task_id"], "task_id")
    for label in ("candidate_artifact", "acceptance_artifact"):
        ref = request[label]
        _exact(ref, ARTIFACT_FIELDS, label)
        _identity(ref["artifact_id"], f"{label}.artifact_id")
        if not isinstance(ref["content_sha256"], str) or not SHA256_RE.fullmatch(ref["content_sha256"]):
            raise ProtocolError(f"invalid {label}.content_sha256")
    _exact(request["runtime"], RUNTIME_FIELDS, "runtime")
    if request["runtime"] != expected_runtime:
        raise ProtocolError("runtime identity mismatch")
    members = request["members"]
    if not isinstance(members, list) or not 1 <= len(members) <= MEMBER_COUNT_LIMIT:
        raise ProtocolError("invalid member count")
    seen = set()
    total = 0
    order = []
    for member in members:
        _exact(member, MEMBER_FIELDS, "member")
        if member["role"] not in {"candidate", "acceptance"}:
            raise ProtocolError("invalid member role")
        path = member["path"]
        if not isinstance(path, str) or not path.isascii() or not PATH_RE.fullmatch(path):
            raise ProtocolError("invalid member path")
        parts = path.split("/")
        if path.startswith("/") or path.endswith("/") or any(p in {"", ".", ".."} for p in parts):
            raise ProtocolError("unsafe member path")
        folded = path.casefold()
        if folded in seen:
            raise ProtocolError("duplicate member path")
        seen.add(folded)
        if not isinstance(member["size"], int) or isinstance(member["size"], bool) or not 0 <= member["size"] <= MEMBER_LIMIT:
            raise ProtocolError("invalid member size")
        if not isinstance(member["sha256"], str) or not SHA256_RE.fullmatch(member["sha256"]):
            raise ProtocolError("invalid member sha256")
        total += member["size"]
        order.append((member["role"], path))
    if total > TOTAL_LIMIT:
        raise ProtocolError("member total exceeds limit")
    if order != sorted(order):
        raise ProtocolError("members are not canonically ordered")
    return tuple(members)


def decode_request(stream, expected_runtime: dict, now=None):
    request = decode_canonical_json(read_frame(stream, REQUEST_LIMIT))
    members = validate_request(request, expected_runtime, now)
    payloads = []
    for member in members:
        payload = read_frame(stream, MEMBER_LIMIT)
        if len(payload) != member["size"]:
            raise ProtocolError("member size mismatch")
        if hashlib.sha256(payload).hexdigest() != member["sha256"]:
            raise ProtocolError("member digest mismatch")
        payloads.append(payload)
    if stream.read(1) != b"":
        raise ProtocolError("trailing input")
    return request, tuple(payloads)
