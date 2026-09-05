import hashlib
import io
import sys
from pathlib import Path

import pytest

TOOLS = Path(__file__).parents[1] / "tools" / "qaos-worker"
sys.path.insert(0, str(TOOLS))
import qaos_worker_probe as probe
from qaos_worker_exchange import canonical_json, decode_request, encode_frame


def response_for(request, **changes):
    empty = hashlib.sha256(b"").hexdigest()
    value = {
        "protocol": request["protocol"], "version": request["version"],
        "request_id": request["request_id"], "nonce": request["nonce"],
        "objective_id": request["objective_id"], "task_id": request["task_id"],
        "candidate_artifact": request["candidate_artifact"],
        "acceptance_artifact": request["acceptance_artifact"],
        "worker_instance_id": "qaos-worker", "launcher_sha256": probe.LAUNCHER_SHA256,
        "runtime_version": probe.RUNTIME_VERSION, "image_digest": probe.IMAGE_DIGEST,
        "policy_id": probe.POLICY_ID, "started_at": request["created_at"],
        "completed_at": request["created_at"], "outcome": "completed",
        "exit_code": 0, "oom_killed": False, "termination_reason": "completion",
        "stdout": {"bytes": 0, "sha256": empty, "truncated": False, "text_preview": ""},
        "stderr": {"bytes": 0, "sha256": empty, "truncated": False, "text_preview": ""},
        "resource_evidence": {"fixture": "harmless", "spec_sha256": "c" * 64},
        "acceptance_results": [{"test_id": "transport.synthetic.harmless", "status": "passed", "duration_ms": 7}],
        "cleanup": {"staging_removed": True, "launcher_cleanup_reported": True},
    }
    value.update(changes)
    value["response_sha256"] = hashlib.sha256(canonical_json(value)).hexdigest()
    return encode_frame(canonical_json(value), probe.RESPONSE_LIMIT)


def test_probe_builds_valid_canonical_two_member_request():
    request, wire = probe.build_probe()
    decoded, payloads = decode_request(io.BytesIO(wire), request["runtime"])
    assert decoded == request
    assert payloads == (
        b"QAOS synthetic acceptance bytes\n", b"QAOS synthetic candidate bytes\n"
    )


def test_response_validation_checks_fields_correlations_runtime_hash_and_eof():
    request, _ = probe.build_probe()
    assert probe.validate_response(response_for(request), request)["outcome"] == "completed"
    for changed, message in [
        ({"request_id": "other"}, "correlation"),
        ({"policy_id": "other"}, "runtime"),
        ({"extra": True}, "fields"),
    ]:
        with pytest.raises(ValueError, match=message):
            probe.validate_response(response_for(request, **changed), request)
    tampered = bytearray(response_for(request)); tampered[-2] ^= 1
    with pytest.raises(Exception):
        probe.validate_response(bytes(tampered), request)
    with pytest.raises(ValueError, match="trailing"):
        probe.validate_response(response_for(request) + b"x", request)


@pytest.mark.parametrize("changed, message", [
    ({"worker_instance_id": "other"}, "identity"), ({"runtime_version": "other"}, "identity"),
    ({"outcome": "unknown"}, "outcome"), ({"completed_at": "2026-09-05T11:59:59Z"}, "timestamp order"),
    ({"exit_code": 1}, "execution"), ({"oom_killed": True}, "execution"),
    ({"termination_reason": "deadline"}, "execution"),
    ({"cleanup": {"staging_removed": False, "launcher_cleanup_reported": True}}, "cleanup"),
    ({"cleanup": {"staging_removed": True}}, "cleanup"),
    ({"resource_evidence": {"fixture": "other", "spec_sha256": "c" * 64}}, "resource"),
    ({"acceptance_results": []}, "acceptance"),
    ({"acceptance_results": [{"test_id": "transport.synthetic.harmless", "status": "failed", "duration_ms": 7}]}, "acceptance"),
    ({"stdout": {"bytes": -1, "sha256": "0" * 64, "truncated": False, "text_preview": ""}}, "stream"),
])
def test_completed_response_acceptance_is_fail_closed(changed, message):
    request, _ = probe.build_probe(now=probe.datetime(2026, 9, 5, 12, 0, tzinfo=probe.timezone.utc))
    with pytest.raises(ValueError, match=message):
        probe.validate_response(response_for(request, **changed), request)


def test_ssh_uses_only_dedicated_key_and_disables_interactive_auth(monkeypatch):
    captured = {}
    def fake_run(command, **kwargs):
        captured["command"] = command
        return type("Result", (), {"returncode": 1, "stdout": b"", "stderr": b""})()
    monkeypatch.setattr(probe.subprocess, "run", fake_run)
    probe.ssh_exchange("host", "dedicated-key", "known-hosts", b"wire")
    joined = " ".join(captured["command"])
    for option in ("IdentitiesOnly=yes", "PasswordAuthentication=no", "KbdInteractiveAuthentication=no", "PreferredAuthentications=publickey"):
        assert option in joined
    assert "-i dedicated-key" in joined
