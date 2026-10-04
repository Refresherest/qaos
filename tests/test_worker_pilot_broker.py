"""Local-only broker tests for the fixed Python pilot policy (WO-174)."""

import io
import json
import stat
import sys
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace

import pytest

TOOLS = Path(__file__).parents[1] / "tools" / "qaos-worker"
sys.path.insert(0, str(TOOLS))

import qaos_worker_broker as broker
import qaos_worker_exchange as exchange
import qaos_worker_pilot as pilot_controller
from tests.test_worker_exchange_protocol import NOW, request

VERIFY_PILOT_METADATA = broker.verify_pilot_launcher_metadata


ACCEPTANCE = b"assert True  # independent test fixture, never executed here\n"
CANDIDATE = b"print('candidate fixture, never executed here')\n"


@pytest.fixture
def pilot_config(tmp_path, monkeypatch):
    harmless_launcher = tmp_path / "harmless-launcher"
    harmless_launcher.write_bytes(b"synthetic trusted launcher")
    pilot_launcher = tmp_path / "python-single-launcher"
    pilot_launcher.write_bytes(b"pilot trusted launcher")
    pilot_runtime = {
        "launcher_sha256": broker.sha256_bytes(pilot_launcher.read_bytes()),
        "image_digest": broker.IMAGE_DIGEST,
        "policy_id": broker.PILOT_POLICY_ID,
    }
    config = broker.BrokerConfig(
        launcher=harmless_launcher,
        replay_root=tmp_path / "replay",
        staging_root=tmp_path / "staging",
        lock_path=tmp_path / "run" / "active.lock",
        worker_instance_id="test-worker",
        expected_runtime={
            "launcher_sha256": broker.sha256_bytes(harmless_launcher.read_bytes()),
            "image_digest": broker.IMAGE_DIGEST,
            "policy_id": broker.POLICY_ID,
        },
        pilot_launcher=pilot_launcher,
        expected_pilot_runtime=pilot_runtime,
        pilot_spec_sha256="c" * 64,
    )
    monkeypatch.setattr(
        broker,
        "fcntl",
        SimpleNamespace(LOCK_EX=1, LOCK_NB=2, flock=lambda *unused: None),
    )
    monkeypatch.setattr(broker.os, "O_NOFOLLOW", 0, raising=False)
    monkeypatch.setattr(broker, "fsync_directory", lambda unused: None)
    monkeypatch.setattr(broker, "PILOT_LAUNCHER_PATH", pilot_launcher)
    monkeypatch.setattr(broker, "verify_pilot_launcher_metadata", lambda unused: None)
    return config


def pilot_request(config, acceptance=ACCEPTANCE, candidate=CANDIDATE):
    value, _ = request()
    value["runtime"] = config.expected_pilot_runtime
    value["acceptance_artifact"] = {
        "artifact_id": "acceptance-artifact",
        "content_sha256": broker.sha256_bytes(acceptance),
    }
    value["candidate_artifact"] = {
        "artifact_id": "candidate-artifact",
        "content_sha256": broker.sha256_bytes(candidate),
    }
    payloads = (acceptance, candidate)
    value["members"] = [
        {
            "role": role,
            "path": path,
            "size": len(payload),
            "sha256": broker.sha256_bytes(payload),
        }
        for role, path, payload in (
            ("acceptance", "acceptance/acceptance.py", acceptance),
            ("candidate", "candidate/candidate.py", candidate),
        )
    ]
    return value, payloads


def wire(request_value, payloads):
    framed = exchange.encode_frame(
        exchange.canonical_json(request_value), exchange.REQUEST_LIMIT
    )
    for payload in payloads:
        framed += exchange.encode_frame(payload, exchange.MEMBER_LIMIT)
    return io.BytesIO(framed)


def response_from(output):
    stream = io.BytesIO(output.getvalue())
    response = exchange.decode_canonical_json(
        exchange.read_frame(stream, broker.RESPONSE_LIMIT)
    )
    assert stream.read(1) == b""
    response_digest = response.pop("response_sha256")
    assert response_digest == broker.sha256_bytes(exchange.canonical_json(response))
    return response


def pilot_evidence(config, passed=True):
    stdout = b"accepted\n" if passed else b"failed\n"
    return {
        "fixture": "python-single",
        "image": config.expected_pilot_runtime["image_digest"],
        "spec_sha256": config.pilot_spec_sha256,
        "expected_pass": passed,
        "exit_code": 0 if passed else 7,
        "docker_cli_exit": 0 if passed else 7,
        "oom_killed": False,
        "reason": "completion",
        "stdout_bytes": len(stdout),
        "stdout_sha256": broker.sha256_bytes(stdout),
        "stdout_preview": stdout.decode(),
        "stderr_bytes": 0,
        "stderr_sha256": broker.sha256_bytes(b""),
        "stderr_preview": "",
    }


@pytest.mark.parametrize("passed, outcome, status", [
    (True, "completed", "passed"),
    (False, "candidate_failed", "failed"),
])
def test_pilot_dispatch_uses_exact_staged_members_and_cleans(
    pilot_config, monkeypatch, passed, outcome, status
):
    config = pilot_config
    value, payloads = pilot_request(config)
    observed = []

    def fake_run_pilot(received_config, staging):
        assert received_config is config
        assert (staging / "acceptance" / "acceptance.py").read_bytes() == ACCEPTANCE
        assert (staging / "candidate" / "candidate.py").read_bytes() == CANDIDATE
        observed.append(staging)
        return pilot_evidence(config, passed), 7

    monkeypatch.setattr(broker, "run_pilot", fake_run_pilot)
    monkeypatch.setattr(
        broker,
        "run_harmless",
        lambda unused: pytest.fail("pilot may not use the synthetic launcher"),
    )
    output = io.BytesIO()
    broker.process(wire(value, payloads), output, config, NOW)
    response = response_from(output)

    assert len(observed) == 1
    assert response["outcome"] == outcome
    assert response["request_id"] == value["request_id"]
    assert response["candidate_artifact"] == value["candidate_artifact"]
    assert response["acceptance_artifact"] == value["acceptance_artifact"]
    assert response["policy_id"] == broker.PILOT_POLICY_ID
    assert response["resource_evidence"] == {
        "fixture": "python-single", "spec_sha256": config.pilot_spec_sha256,
    }
    assert response["acceptance_results"] == [{
        "test_id": "pilot.python-single.acceptance",
        "status": status,
        "duration_ms": 7,
    }]
    assert response["cleanup"] == {
        "staging_removed": True, "launcher_cleanup_reported": True,
    }
    assert response["stdout"]["truncated"] is False
    assert response["stderr"]["truncated"] is False
    assert list(config.staging_root.iterdir()) == []
    assert len(list(config.replay_root.iterdir())) == 1


@pytest.mark.parametrize("reason, oom_killed", [
    ("deadline", False),
    ("stdout_limit", False),
    ("oom", True),
])
def test_pilot_limit_evidence_returns_limit_terminated_and_cleans(
    pilot_config, monkeypatch, reason, oom_killed
):
    value, payloads = pilot_request(pilot_config)
    evidence = pilot_evidence(pilot_config, passed=False)
    evidence.update(
        reason=reason, oom_killed=oom_killed, exit_code=137,
        docker_cli_exit=137,
    )

    def fake_subprocess_run(argv, **unused):
        assert argv[1] == "python-single"
        return SimpleNamespace(
            returncode=1,
            stdout=json.dumps(evidence).encode("utf-8"),
            stderr=b"",
        )

    monkeypatch.setattr(
        broker.subprocess, "run", fake_subprocess_run
    )
    output = io.BytesIO()
    broker.process(wire(value, payloads), output, pilot_config, NOW)
    response = response_from(output)
    assert response["outcome"] == "limit_terminated"
    assert response["termination_reason"] == reason
    assert response["acceptance_results"] == []
    assert response["stdout"]["truncated"] is True
    assert response["stderr"]["truncated"] is True
    assert response["cleanup"] == {
        "staging_removed": True, "launcher_cleanup_reported": True,
    }
    assert list(pilot_config.staging_root.iterdir()) == []


@pytest.mark.parametrize("mutate", [
    lambda value: value["members"].pop(),
    lambda value: value["members"].append(dict(value["members"][1], path="candidate/other.py")),
    lambda value: value["members"][0].update(role="candidate"),
    lambda value: value["members"][0].update(path="acceptance/other.py"),
    lambda value: value["members"][1].update(path="candidate/other.py"),
])
def test_pilot_requires_exact_two_roles_and_paths(pilot_config, mutate):
    value, payloads = pilot_request(pilot_config)
    mutate(value)
    with pytest.raises(broker.ProtocolError, match="two exact fixed members"):
        broker.validate_pilot_request(value, payloads)


@pytest.mark.parametrize("change", [
    lambda value: value["candidate_artifact"].update(content_sha256="0" * 64),
    lambda value: value["acceptance_artifact"].update(content_sha256="0" * 64),
    lambda value: value["acceptance_artifact"].update(artifact_id="candidate-artifact"),
])
def test_pilot_rejects_artifact_mismatch_and_self_acceptance(pilot_config, change):
    value, payloads = pilot_request(pilot_config)
    change(value)
    with pytest.raises(broker.ProtocolError):
        broker.validate_pilot_request(value, payloads)


@pytest.mark.parametrize("payload, role", [
    (b"", "candidate"),
    (b"\xff", "candidate"),
    (b"x" * (broker.PILOT_FILE_LIMIT + 1), "candidate"),
    (b"", "acceptance"),
    (b"\xff", "acceptance"),
    (b"x" * (broker.PILOT_FILE_LIMIT + 1), "acceptance"),
], ids=[
    "empty-candidate", "invalid-utf8-candidate", "oversize-candidate",
    "empty-acceptance", "invalid-utf8-acceptance", "oversize-acceptance",
])
def test_pilot_enforces_nonempty_utf8_file_cap(pilot_config, payload, role):
    kwargs = {role: payload}
    value, payloads = pilot_request(pilot_config, **kwargs)
    with pytest.raises(broker.ProtocolError, match="bounds|UTF-8"):
        broker.validate_pilot_request(value, payloads)


@pytest.mark.parametrize("change", [
    lambda value: value["candidate_artifact"].update(content_sha256="0" * 64),
    lambda value: value["members"][0].update(path="acceptance/other.py"),
])
def test_invalid_pilot_is_refused_before_replay_or_staging(
    pilot_config, monkeypatch, change
):
    value, payloads = pilot_request(pilot_config)
    change(value)
    monkeypatch.setattr(
        broker,
        "run_pilot",
        lambda *unused: pytest.fail("invalid pilot must not launch"),
    )
    with pytest.raises(broker.ProtocolError):
        broker.process(wire(value, payloads), io.BytesIO(), pilot_config, NOW)
    assert not pilot_config.replay_root.exists()
    assert not pilot_config.staging_root.exists()


def test_protocol_accepts_only_configured_pilot_runtime(pilot_config):
    value, _ = pilot_request(pilot_config)
    allowed = pilot_config.allowed_runtimes()
    assert exchange.validate_request(value, allowed, NOW) == tuple(value["members"])
    value["runtime"] = dict(value["runtime"], policy_id="caller-selected")
    with pytest.raises(exchange.ProtocolError, match="runtime identity mismatch"):
        exchange.validate_request(value, allowed, NOW)


def test_pilot_disabled_by_default_refuses_before_staging(pilot_config, monkeypatch):
    configured = pilot_config
    config = broker.BrokerConfig(
        launcher=configured.launcher,
        replay_root=configured.replay_root,
        staging_root=configured.staging_root,
        lock_path=configured.lock_path,
        expected_runtime=configured.runtime(),
    )
    value, payloads = pilot_request(configured)
    monkeypatch.setattr(
        broker,
        "run_pilot",
        lambda *unused: pytest.fail("disabled pilot must not launch"),
    )
    with pytest.raises(broker.ProtocolError, match="runtime identity mismatch"):
        broker.process(wire(value, payloads), io.BytesIO(), config, NOW)
    assert not config.staging_root.exists()
    assert not config.replay_root.exists()


def test_installed_pilot_switch_absent_preserves_synthetic_default():
    class MissingPath:
        def lstat(self):
            raise FileNotFoundError

    config = broker.installed_config(MissingPath())
    assert config.allowed_runtimes() == config.runtime()
    assert config.pilot_launcher is None


def test_installed_pilot_switch_requires_exact_root_owned_bytes():
    parent = MetadataPath(stat.S_IFDIR | 0o755)

    class EnablePath(MetadataPath):
        def __init__(self, mode, payload, *, uid=0, nlink=1, parents=(parent,)):
            super().__init__(mode, uid=uid, nlink=nlink, parents=parents)
            self.payload = payload

        def read_bytes(self):
            return self.payload

    enabled = broker.installed_config(
        EnablePath(stat.S_IFREG | 0o400, broker.PILOT_ENABLE_BYTES)
    )
    assert enabled.pilot_launcher == broker.PILOT_LAUNCHER_PATH
    assert enabled.expected_pilot_runtime == {
        "launcher_sha256": broker.PILOT_LAUNCHER_SHA256,
        "image_digest": broker.IMAGE_DIGEST,
        "policy_id": broker.PILOT_POLICY_ID,
    }
    assert enabled.pilot_spec_sha256 == broker.PILOT_SPEC_SHA256
    assert enabled.allowed_runtimes() == (
        enabled.runtime(), enabled.expected_pilot_runtime,
    )
    assert broker.PILOT_LAUNCHER_SHA256 == pilot_controller.PILOT_LAUNCHER_SHA256
    assert broker.PILOT_SPEC_SHA256 == pilot_controller.PILOT_SPEC_SHA256
    assert broker.sha256_bytes(
        (TOOLS / "qaos_worker_pilot_launcher.py").read_bytes()
    ) == broker.PILOT_LAUNCHER_SHA256

    bad_paths = (
        EnablePath(stat.S_IFREG | 0o400, b"wrong\n"),
        EnablePath(stat.S_IFREG | 0o444, broker.PILOT_ENABLE_BYTES),
        EnablePath(stat.S_IFREG | 0o400, broker.PILOT_ENABLE_BYTES, uid=1000),
        EnablePath(stat.S_IFREG | 0o400, broker.PILOT_ENABLE_BYTES, nlink=2),
        EnablePath(stat.S_IFLNK | 0o400, broker.PILOT_ENABLE_BYTES),
        EnablePath(
            stat.S_IFREG | 0o400, broker.PILOT_ENABLE_BYTES,
            parents=(MetadataPath(stat.S_IFDIR | 0o777),),
        ),
    )
    for path in bad_paths:
        with pytest.raises(RuntimeError, match="pilot enable"):
            broker.installed_config(path)


def test_partial_pilot_configuration_is_refused(pilot_config):
    config = broker.BrokerConfig(
        launcher=pilot_config.launcher,
        expected_runtime=pilot_config.runtime(),
        pilot_launcher=pilot_config.pilot_launcher,
        expected_pilot_runtime=pilot_config.expected_pilot_runtime,
    )
    with pytest.raises(RuntimeError, match="not fully pinned"):
        config.allowed_runtimes()


def test_pilot_launcher_path_is_fixed_even_with_matching_hash(pilot_config):
    alternative = pilot_config.pilot_launcher.with_name("alternate-launcher")
    alternative.write_bytes(pilot_config.pilot_launcher.read_bytes())
    config = replace(pilot_config, pilot_launcher=alternative)
    with pytest.raises(RuntimeError, match="not fully pinned"):
        config.allowed_runtimes()
    with pytest.raises(broker.RuntimeFailure, match="path is not pinned"):
        broker.verify_launcher(config, pilot=True)


class MetadataPath:
    def __init__(self, mode, *, uid=0, nlink=1, parents=()):
        self.parents = parents
        self.info = SimpleNamespace(st_mode=mode, st_uid=uid, st_nlink=nlink)

    def lstat(self):
        return self.info


@pytest.mark.parametrize("file_mode, uid, nlink", [
    (stat.S_IFREG | 0o775, 0, 1),
    (stat.S_IFREG | 0o755, 1000, 1),
    (stat.S_IFREG | 0o755, 0, 2),
    (stat.S_IFLNK | 0o755, 0, 1),
    (stat.S_IFREG | 0o644, 0, 1),
])
def test_pilot_launcher_metadata_rejects_unsafe_file(file_mode, uid, nlink):
    safe_parent = MetadataPath(stat.S_IFDIR | 0o755)
    path = MetadataPath(file_mode, uid=uid, nlink=nlink, parents=(safe_parent,))
    with pytest.raises(broker.RuntimeFailure, match="path is not root-owned"):
        VERIFY_PILOT_METADATA(path)


@pytest.mark.parametrize("parent_mode, uid", [
    (stat.S_IFDIR | 0o777, 0),
    (stat.S_IFDIR | 0o755, 1000),
    (stat.S_IFLNK | 0o755, 0),
])
def test_pilot_launcher_metadata_rejects_unsafe_parent(parent_mode, uid):
    parent = MetadataPath(parent_mode, uid=uid)
    path = MetadataPath(stat.S_IFREG | 0o755, parents=(parent,))
    with pytest.raises(broker.RuntimeFailure, match="directory is not root-owned"):
        VERIFY_PILOT_METADATA(path)


def test_pilot_launcher_metadata_accepts_root_owned_fixed_path():
    parent = MetadataPath(stat.S_IFDIR | 0o755)
    path = MetadataPath(stat.S_IFREG | 0o755, parents=(parent,))
    VERIFY_PILOT_METADATA(path)


def test_pilot_launcher_metadata_refusal_prevents_execution(pilot_config, monkeypatch):
    monkeypatch.setattr(
        broker, "verify_pilot_launcher_metadata",
        lambda unused: (_ for _ in ()).throw(
            broker.RuntimeFailure("pilot launcher path is not root-owned and fixed")
        ),
    )
    with pytest.raises(broker.RuntimeFailure, match="not root-owned"):
        broker.verify_launcher(pilot_config, pilot=True)


def test_enabled_pilot_preserves_synthetic_harmless_dispatch(pilot_config, monkeypatch):
    config = pilot_config
    value, payload = request()
    value["runtime"] = config.runtime()
    evidence = dict(pilot_evidence(config), fixture="harmless")
    monkeypatch.setattr(broker, "run_harmless", lambda unused: (evidence, 5))
    monkeypatch.setattr(
        broker,
        "run_pilot",
        lambda *unused: pytest.fail("synthetic request may not use pilot launcher"),
    )
    output = io.BytesIO()
    broker.process(wire(value, (payload,)), output, config, NOW)
    response = response_from(output)
    assert response["outcome"] == "completed"
    assert response["policy_id"] == config.runtime()["policy_id"]
    assert response["resource_evidence"]["fixture"] == "harmless"
    assert response["acceptance_results"][0]["test_id"] == "transport.synthetic.harmless"


def test_pilot_launcher_invocation_is_fixed_and_evidence_is_checked(
    pilot_config, monkeypatch
):
    config = pilot_config
    staging = config.staging_root / "request-fixed"
    observed = []

    def fake_subprocess_run(argv, **kwargs):
        observed.append((argv, kwargs))
        return SimpleNamespace(
            returncode=0,
            stdout=json.dumps(pilot_evidence(config)).encode("utf-8"),
            stderr=b"",
        )

    monkeypatch.setattr(broker.subprocess, "run", fake_subprocess_run)
    evidence, duration = broker.run_pilot(config, staging)
    assert evidence["fixture"] == "python-single"
    assert duration >= 0
    assert observed[0][0] == [str(config.pilot_launcher), "python-single", str(staging)]
    assert observed[0][1]["stdin"] is broker.subprocess.DEVNULL
    assert observed[0][1]["timeout"] == 90


@pytest.mark.parametrize("mutation", [
    lambda evidence: evidence.update(spec_sha256="0" * 64),
    lambda evidence: evidence.update(expected_pass="true"),
    lambda evidence: evidence.update(stdout_bytes=True),
    lambda evidence: evidence.update(image="unapproved-image"),
    lambda evidence: evidence.update(docker_cli_exit=True),
    lambda evidence: evidence.update(docker_cli_exit=None),
    lambda evidence: evidence.update(reason="deadline"),
    lambda evidence: evidence.update(exit_code=7),
    lambda evidence: evidence.update(oom_killed=True),
])
def test_pilot_launcher_rejects_untrusted_evidence(
    pilot_config, monkeypatch, mutation
):
    evidence = pilot_evidence(pilot_config)
    mutation(evidence)
    monkeypatch.setattr(
        broker.subprocess,
        "run",
        lambda *args, **kwargs: SimpleNamespace(
            returncode=0, stdout=json.dumps(evidence).encode("utf-8"), stderr=b""
        ),
    )
    with pytest.raises(broker.CleanupError, match="evidence|stream"):
        broker.run_pilot(pilot_config, pilot_config.staging_root / "request-fixed")


@pytest.mark.parametrize("failure", ["malformed-json", "timeout"])
def test_post_invocation_untrusted_pilot_response_is_cleanup_failed(
    pilot_config, monkeypatch, failure
):
    value, payloads = pilot_request(pilot_config)

    def fake_subprocess_run(argv, **unused):
        assert argv[1] == "python-single"
        if failure == "timeout":
            raise broker.subprocess.TimeoutExpired(argv, 90)
        return SimpleNamespace(returncode=0, stdout=b"not-json", stderr=b"")

    monkeypatch.setattr(broker.subprocess, "run", fake_subprocess_run)
    output = io.BytesIO()
    broker.process(wire(value, payloads), output, pilot_config, NOW)
    response = response_from(output)
    assert response["outcome"] == "cleanup_failed"
    assert response["termination_reason"] == "cleanup_failed"
    assert response["acceptance_results"] == []
    assert response["cleanup"] == {
        "staging_removed": True,
        "launcher_cleanup_reported": False,
    }
    assert list(pilot_config.staging_root.iterdir()) == []
