import io
import json
import os
import sys
from types import SimpleNamespace
from pathlib import Path

import pytest

TOOLS = Path(__file__).parents[1] / "tools" / "qaos-worker"
sys.path.insert(0, str(TOOLS))
import qaos_worker_broker as broker
from tests.test_worker_exchange_protocol import NOW, RUNTIME, framed, request


@pytest.fixture
def config(tmp_path, monkeypatch):
    launcher = tmp_path / "launcher"
    launcher.write_bytes(b"trusted launcher")
    runtime = dict(RUNTIME, launcher_sha256=broker.sha256_bytes(launcher.read_bytes()))
    cfg = broker.BrokerConfig(
        launcher=launcher, replay_root=tmp_path / "replay",
        staging_root=tmp_path / "staging", lock_path=tmp_path / "run" / "active.lock",
        worker_instance_id="test-worker", expected_runtime=runtime,
    )
    evidence = {
        "fixture": "harmless", "expected_pass": True, "exit_code": 0,
        "oom_killed": False, "reason": "completion", "stdout_bytes": 3,
        "stdout_sha256": broker.sha256_bytes(b"ok\n"), "stdout_preview": "ok\n",
        "stderr_bytes": 0, "stderr_sha256": broker.sha256_bytes(b""),
        "stderr_preview": "", "spec_sha256": "c" * 64,
    }
    monkeypatch.setattr(broker, "run_harmless", lambda unused: (evidence, 7))
    return cfg


@pytest.fixture
def ready(config, monkeypatch):
    monkeypatch.setattr(
        broker,
        "fcntl",
        SimpleNamespace(LOCK_EX=1, LOCK_NB=2, flock=lambda *unused: None),
    )
    monkeypatch.setattr(broker.os, "O_NOFOLLOW", 0, raising=False)
    monkeypatch.setattr(broker, "fsync_directory", lambda unused: None)
    return config


def input_for(config, payload=b"safe synthetic bytes"):
    value, payload = request(payload)
    value["runtime"] = config.runtime()
    return value, framed(value, payload)


def decode_response(output):
    raw = io.BytesIO(output.getvalue())
    payload = broker.read_frame(raw, broker.RESPONSE_LIMIT) if hasattr(broker, "read_frame") else None
    if payload is None:
        from qaos_worker_exchange import read_frame
        payload = read_frame(raw, broker.RESPONSE_LIMIT)
    return json.loads(payload)


def test_success_claims_replay_stages_runs_and_cleans(ready):
    config = ready
    value, source = input_for(config)
    output = io.BytesIO()
    broker.process(source, output, config, NOW)
    response = decode_response(output)
    assert response["outcome"] == "completed"
    assert response["request_id"] == value["request_id"]
    assert response["acceptance_results"][0]["test_id"] == "transport.synthetic.harmless"
    claimed = list(config.replay_root.iterdir())
    assert len(claimed) == 1
    if os.name != "nt":
        assert claimed[0].stat().st_mode & 0o777 == 0o600
    assert list(config.staging_root.iterdir()) == []
    digest = response.pop("response_sha256")
    assert digest == broker.sha256_bytes(broker.canonical_json(response))


def test_replay_is_rejected_without_new_staging(ready):
    config = ready
    _, source = input_for(config); broker.process(source, io.BytesIO(), config, NOW)
    _, replay = input_for(config)
    output = io.BytesIO(); broker.process(replay, output, config, NOW)
    assert decode_response(output)["outcome"] == "policy_rejected"
    assert list(config.staging_root.iterdir()) == []


def test_launcher_digest_mismatch_cleans_staging(ready):
    config = ready
    value, source = input_for(config)
    config.launcher.write_bytes(b"changed")
    output = io.BytesIO(); broker.process(source, output, config, NOW)
    assert decode_response(output)["outcome"] == "runtime_failed"
    assert list(config.staging_root.iterdir()) == []


def test_launcher_failure_cleans_staging(ready, monkeypatch):
    config = ready
    _, source = input_for(config)
    monkeypatch.setattr(broker, "run_harmless", lambda unused: (_ for _ in ()).throw(broker.RuntimeFailure("failed")))
    output = io.BytesIO(); broker.process(source, output, config, NOW)
    assert decode_response(output)["outcome"] == "runtime_failed"
    assert list(config.staging_root.iterdir()) == []


def test_active_lock_rejects_concurrency(config):
    if os.name == "nt":
        pytest.skip("real flock verification runs on the Linux worker")
    lock = broker.acquire_lock(config)
    try:
        with pytest.raises(broker.ProtocolError, match="active"):
            broker.acquire_lock(config)
    finally:
        lock.close()


def test_main_requires_root(monkeypatch):
    monkeypatch.setattr(broker.os, "geteuid", lambda: 1000, raising=False)
    assert broker.main() == 2


def test_partial_staging_failure_self_cleans(ready, monkeypatch):
    config = ready
    original = broker.write_member
    calls = []
    def fail_after_write(root, member, payload):
        original(root, member, payload); calls.append(True); raise OSError("synthetic write failure")
    monkeypatch.setattr(broker, "write_member", fail_after_write)
    _, source = input_for(config)
    output = io.BytesIO(); broker.process(source, output, config, NOW)
    assert decode_response(output)["outcome"] == "runtime_failed"
    assert list(config.staging_root.iterdir()) == []


def test_staging_directory_permission_failure_self_cleans(ready, monkeypatch):
    config = ready
    original = Path.chmod
    def fail_request_root(path, mode):
        if path.name.startswith("request-"):
            raise OSError("synthetic chmod failure")
        return original(path, mode)
    monkeypatch.setattr(Path, "chmod", fail_request_root)
    _, source = input_for(config)
    output = io.BytesIO(); broker.process(source, output, config, NOW)
    assert decode_response(output)["outcome"] == "runtime_failed"
    assert list(config.staging_root.iterdir()) == []


def test_cleanup_failure_dominates_result(ready, monkeypatch):
    config = ready
    monkeypatch.setattr(broker, "cleanup_staging", lambda unused: (_ for _ in ()).throw(OSError("cleanup")))
    _, source = input_for(config)
    output = io.BytesIO(); broker.process(source, output, config, NOW)
    response = decode_response(output)
    assert response["outcome"] == "cleanup_failed"
    assert response["cleanup"]["staging_removed"] is False


@pytest.mark.parametrize("failure", ["open", "directory_fsync"])
def test_replay_storage_failures_return_correlated_runtime_failure(
    ready, monkeypatch, failure
):
    config = ready
    if failure == "open":
        original = broker.os.open
        monkeypatch.setattr(
            broker.os,
            "open",
            lambda path, *args, **kwargs: (
                (_ for _ in ()).throw(OSError("replay open"))
                if Path(path).parent == config.replay_root
                else original(path, *args, **kwargs)
            ),
        )
    else:
        monkeypatch.setattr(
            broker,
            "fsync_directory",
            lambda unused: (_ for _ in ()).throw(OSError("directory fsync")),
        )
    value, source = input_for(config)
    output = io.BytesIO(); broker.process(source, output, config, NOW)
    response = decode_response(output)
    assert response["outcome"] == "runtime_failed"
    assert response["request_id"] == value["request_id"]


def test_replay_root_preparation_failure_is_correlated(ready, monkeypatch):
    config = ready
    original = broker.ensure_private_directory
    monkeypatch.setattr(
        broker,
        "ensure_private_directory",
        lambda path: (
            (_ for _ in ()).throw(OSError("replay root"))
            if path == config.replay_root else original(path)
        ),
    )
    value, source = input_for(config)
    output = io.BytesIO(); broker.process(source, output, config, NOW)
    response = decode_response(output)
    assert response["outcome"] == "runtime_failed"
    assert response["request_id"] == value["request_id"]
