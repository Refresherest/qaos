import base64
import hashlib
import importlib.util
import io
import sys
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

PATH = Path(__file__).parents[1] / "tools" / "qaos-worker" / "qaos_worker_exchange.py"
SPEC = importlib.util.spec_from_file_location("qaos_worker_exchange", PATH)
exchange = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = exchange
SPEC.loader.exec_module(exchange)

RUNTIME = {"launcher_sha256": "a" * 64, "image_digest": "image@sha256:" + "b" * 64, "policy_id": "synthetic-v1"}
NOW = datetime(2026, 9, 5, 12, 0, tzinfo=timezone.utc)


def request(payload=b"safe synthetic bytes"):
    digest = hashlib.sha256(payload).hexdigest()
    value = {
        "protocol": exchange.PROTOCOL, "version": 1,
        "request_id": str(uuid.UUID("12345678-1234-4234-8234-123456789abc")),
        "nonce": base64.urlsafe_b64encode(b"n" * 32).decode().rstrip("="),
        "created_at": "2026-09-05T11:59:00Z", "expires_at": "2026-09-05T12:01:00Z",
        "objective_id": "objective-1", "task_id": "task-1",
        "candidate_artifact": {"artifact_id": "artifact-1", "content_sha256": digest},
        "acceptance_artifact": {"artifact_id": "artifact-2", "content_sha256": digest},
        "members": [{"role": "candidate", "path": "input.txt", "size": len(payload), "sha256": digest}],
        "runtime": dict(RUNTIME),
    }
    return value, payload


def framed(value, payload, tail=b""):
    return io.BytesIO(exchange.encode_frame(exchange.canonical_json(value), exchange.REQUEST_LIMIT) + exchange.encode_frame(payload, exchange.MEMBER_LIMIT) + tail)


def test_canonical_round_trip_validates_hash_and_eof():
    value, payload = request()
    decoded, payloads = exchange.decode_request(framed(value, payload), RUNTIME, NOW)
    assert decoded == value
    assert payloads == (payload,)


@pytest.mark.parametrize("change, message", [
    (lambda v: v.update(extra=True), "invalid request fields"),
    (lambda v: v["runtime"].update(policy_id="caller-choice"), "runtime identity mismatch"),
    (lambda v: v["members"][0].update(path="../escape"), "unsafe member path"),
    (lambda v: v["members"][0].update(sha256="0" * 64), "member digest mismatch"),
    (lambda v: v.update(expires_at="2026-09-05T12:10:00Z"), "validity exceeds"),
])
def test_invalid_requests_fail_closed(change, message):
    value, payload = request()
    change(value)
    with pytest.raises(exchange.ProtocolError, match=message):
        exchange.decode_request(framed(value, payload), RUNTIME, NOW)


def test_noncanonical_duplicate_and_trailing_input_fail_closed():
    value, payload = request()
    pretty = json_bytes = __import__("json").dumps(value).encode()
    with pytest.raises(exchange.ProtocolError, match="not canonical"):
        exchange.decode_canonical_json(pretty)
    duplicate = b'{"a":1,"a":2}'
    with pytest.raises(exchange.ProtocolError, match="duplicate JSON key"):
        exchange.decode_canonical_json(duplicate)
    with pytest.raises(exchange.ProtocolError, match="trailing input"):
        exchange.decode_request(framed(value, payload, b"x"), RUNTIME, NOW)


def test_frame_bounds_and_early_eof_fail_closed():
    with pytest.raises(exchange.ProtocolError, match="exceeds"):
        exchange.encode_frame(b"xx", 1)
    with pytest.raises(exchange.ProtocolError, match="header EOF"):
        exchange.read_frame(io.BytesIO(b"short"), 10)
    with pytest.raises(exchange.ProtocolError, match="payload EOF"):
        exchange.read_frame(io.BytesIO((5).to_bytes(8, "big") + b"x"), 10)


class Fragmented(io.BytesIO):
    def read(self, size=-1):
        return super().read(min(size, 2) if size >= 0 else size)


def test_fragmented_reads_are_assembled_exactly():
    assert exchange.read_frame(Fragmented(exchange.encode_frame(b"value", 5)), 5) == b"value"


@pytest.mark.parametrize("bad", [
    "12345678-1234-1234-8234-123456789abc",
    "12345678-1234-4234-8234-123456789ABC",
    "not-a-uuid",
])
def test_request_id_must_be_lowercase_uuid4(bad):
    value, _ = request(); value["request_id"] = bad
    with pytest.raises(exchange.ProtocolError, match="request_id"):
        exchange.validate_request(value, RUNTIME, NOW)


@pytest.mark.parametrize("bad", ["", "abc=", "!" * 43, base64.urlsafe_b64encode(b"x" * 31).decode().rstrip("=")])
def test_nonce_must_be_canonical_unpadded_32_bytes(bad):
    value, _ = request(); value["nonce"] = bad
    with pytest.raises(exchange.ProtocolError, match="nonce"):
        exchange.validate_request(value, RUNTIME, NOW)


@pytest.mark.parametrize("created, expires, message", [
    ("2026-09-05T11:54:59Z", "2026-09-05T11:59:59Z", "validity window"),
    ("2026-09-05T12:00:01Z", "2026-09-05T12:01:00Z", "validity window"),
    ("2026-09-05T12:01:00Z", "2026-09-05T12:00:00Z", "validity window"),
    ("2026-09-05 12:00:00Z", "2026-09-05T12:01:00Z", "created_at"),
])
def test_time_window_failures(created, expires, message):
    value, _ = request(); value.update(created_at=created, expires_at=expires)
    with pytest.raises(exchange.ProtocolError, match=message):
        exchange.validate_request(value, RUNTIME, NOW)


def test_exact_five_minute_window_is_allowed():
    value, _ = request(); value.update(created_at="2026-09-05T12:00:00Z", expires_at="2026-09-05T12:05:00Z")
    exchange.validate_request(value, RUNTIME, NOW)


@pytest.mark.parametrize("target, mutation", [
    ("candidate_artifact", lambda d: d.pop("artifact_id")),
    ("acceptance_artifact", lambda d: d.update(extra="x")),
    ("runtime", lambda d: d.pop("policy_id")),
    ("member", lambda d: d.update(extra="x")),
])
def test_nested_fields_are_exact(target, mutation):
    value, _ = request()
    obj = value["members"][0] if target == "member" else value[target]
    mutation(obj)
    with pytest.raises(exchange.ProtocolError, match="fields"):
        exchange.validate_request(value, RUNTIME, NOW)


@pytest.mark.parametrize("field, bad", [("artifact_id", ""), ("content_sha256", "A" * 64), ("content_sha256", "0" * 63)])
def test_artifact_reference_values_are_strict(field, bad):
    value, _ = request(); value["candidate_artifact"][field] = bad
    with pytest.raises(exchange.ProtocolError):
        exchange.validate_request(value, RUNTIME, NOW)


@pytest.mark.parametrize("members", [[], [{}] * 33])
def test_member_count_is_bounded(members):
    value, _ = request(); value["members"] = members
    with pytest.raises(exchange.ProtocolError, match="member count"):
        exchange.validate_request(value, RUNTIME, NOW)


@pytest.mark.parametrize("change, message", [
    (lambda m: m.update(role="other"), "role"),
    (lambda m: m.update(size=True), "size"),
    (lambda m: m.update(size=exchange.MEMBER_LIMIT + 1), "size"),
    (lambda m: m.update(path="/root"), "path"),
    (lambda m: m.update(path="tail/"), "path"),
    (lambda m: m.update(path="a//b"), "path"),
    (lambda m: m.update(path="a/./b"), "path"),
    (lambda m: m.update(path="a\\b"), "path"),
    (lambda m: m.update(path="café"), "path"),
    (lambda m: m.update(path="a" * 129), "path"),
])
def test_member_value_boundaries(change, message):
    value, _ = request(); change(value["members"][0])
    with pytest.raises(exchange.ProtocolError, match=message):
        exchange.validate_request(value, RUNTIME, NOW)


def test_member_order_duplicates_and_aggregate_are_rejected():
    value, payload = request()
    base = value["members"][0]
    value["members"] = [dict(base, role="candidate", path="z"), dict(base, role="acceptance", path="a")]
    with pytest.raises(exchange.ProtocolError, match="ordered"):
        exchange.validate_request(value, RUNTIME, NOW)
    value["members"] = [dict(base, role="candidate", path="A"), dict(base, role="acceptance", path="a")]
    with pytest.raises(exchange.ProtocolError, match="duplicate"):
        exchange.validate_request(value, RUNTIME, NOW)
    value["members"] = [dict(base, path=str(i), size=exchange.MEMBER_LIMIT) for i in range(9)]
    with pytest.raises(exchange.ProtocolError, match="total"):
        exchange.validate_request(value, RUNTIME, NOW)


def test_decode_request_enforces_request_frame_limit_and_json_constants():
    oversized = (exchange.REQUEST_LIMIT + 1).to_bytes(8, "big")
    with pytest.raises(exchange.ProtocolError, match="exceeds"):
        exchange.decode_request(io.BytesIO(oversized), RUNTIME, NOW)
    with pytest.raises(exchange.ProtocolError, match="constant"):
        exchange.decode_canonical_json(b'{"value":NaN}')
    with pytest.raises(exchange.ProtocolError, match="Unicode"):
        exchange.decode_canonical_json(b'{"value":"\\ud800"}')
