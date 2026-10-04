"""Local structural tests: never run either a candidate or Docker."""

import hashlib
import json
import os
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

TOOLS = Path(__file__).parents[1] / "tools" / "qaos-worker"
sys.path.insert(0, str(TOOLS))
import qaos_worker_pilot_launcher as pilot


def test_fixed_spec_has_only_two_read_only_source_mounts_and_no_network():
    args = pilot.container_args("qaos-pilot-123", "/run/qaos-worker-broker/staging/request-abcdefgh")
    assert args[:3] == ["create", "--name", "qaos-pilot-123"]
    assert "--pull=never" in args
    assert "--runtime=runsc" in args
    assert "--network=none" in args
    assert "--read-only" in args
    assert "--cpus=1" in args
    assert "--memory=1g" in args
    assert "--memory-swap=1g" in args
    assert "--pids-limit=32" in args
    assert "--cap-drop=ALL" in args
    assert "--security-opt=no-new-privileges" in args
    assert "--user=65534:65534" in args
    assert "--log-driver=none" in args
    assert args.count("--mount") == 2
    assert args[-7:] == [pilot.IMAGE, *pilot.COMMAND]
    assert args[args.index("--mount") + 1].endswith(
        "/candidate/candidate.py,dst=/opt/qaos/candidate/candidate.py,readonly"
    )
    assert args[args.index("--mount", args.index("--mount") + 1) + 1].endswith(
        "/acceptance/acceptance.py,dst=/opt/qaos/acceptance/acceptance.py,readonly"
    )
    assert "--env" not in args and "--entrypoint" not in args


def test_spec_digest_is_stable_across_request_and_container_names():
    normalized = pilot.container_args("<name>", "<stage>")[3:]
    expected = hashlib.sha256(json.dumps(normalized, separators=(",", ":")).encode()).hexdigest()
    assert pilot.PILOT_SPEC_SHA256 == expected
    assert len(expected) == 64


@pytest.mark.parametrize("source", [
    pytest.param(b"", id="empty"),
    pytest.param(b"a" * (64 * 1024 + 1), id="oversized"),
    pytest.param(b"\xff", id="invalid-utf8"),
])
def test_source_rejects_empty_oversized_or_invalid_utf8(source):
    with pytest.raises(ValueError):
        pilot._validate_source_bytes(source)


def test_source_accepts_exact_cap_and_utf8():
    pilot._validate_source_bytes("λ".encode() + b"a" * (64 * 1024 - 2))


def test_prepare_stage_requires_exact_two_file_tree(tmp_path, monkeypatch):
    staging = tmp_path / "staging"
    stage = staging / "request-abcdefgh"
    candidate = stage / "candidate" / "candidate.py"
    acceptance = stage / "acceptance" / "acceptance.py"
    for path in (candidate, acceptance):
        path.parent.mkdir(parents=True)
        path.write_text("pass\n", encoding="utf-8")
    opened = []
    chmods = []
    monkeypatch.setattr(pilot, "_check_directory", lambda *unused, **kwargs: None)
    monkeypatch.setattr(pilot.os, "fchmod", lambda descriptor, mode: chmods.append(mode))

    def fake_open(path):
        opened.append(path)
        return os.open(path, os.O_RDONLY)

    monkeypatch.setattr(pilot, "_open_source", fake_open)
    pilot.prepare_stage(stage, staging_root=staging)
    assert opened == [candidate, acceptance]
    assert chmods == [0o444, 0o444]
    (stage / "extra.py").write_text("pass\n", encoding="utf-8")
    with pytest.raises(ValueError, match="unexpected entries"):
        pilot.prepare_stage(stage, staging_root=staging)


@pytest.mark.parametrize("stage", [
    Path("relative/request-abcdefgh"),
    Path("/run/qaos-worker-broker/staging/request-abcdefgh/../request-abcdefgh"),
    Path("/run/qaos-worker-broker/other/request-abcdefgh"),
    Path("/run/qaos-worker-broker/staging/not-a-request"),
])
def test_stage_path_rejects_unsafe_locations_before_file_access(stage):
    with pytest.raises(ValueError, match="outside the fixed broker"):
        pilot.prepare_stage(stage)


@pytest.mark.parametrize("exit_code,oom,reason,cli,status,error,expected_reason,passed", [
    (0, False, "completion", 0, "exited", "", "completion", True),
    (1, False, "completion", 1, "exited", "", "completion", False),
    (7, False, "completion", 7, "exited", "", "completion", False),
    (137, True, "completion", 137, "exited", "", "oom", False),
    (0, False, "deadline", 0, "running", "", "deadline", False),
    (0, False, "stdout_limit", 1, "dead", "daemon error", "stdout_limit", False),
    (0, False, "completion", 1, "exited", "", "runtime_error", False),
    (1, False, "completion", 0, "exited", "", "runtime_error", False),
    (0, False, "completion", 0, "running", "", "runtime_error", False),
    (0, False, "completion", 0, "dead", "", "runtime_error", False),
    (0, False, "completion", 0, "exited", "daemon failure secret", "runtime_error", False),
    (0, False, "completion", 0, None, None, "runtime_error", False),
])
def test_pilot_returns_bounded_structured_evidence_and_cleans(
    monkeypatch, exit_code, oom, reason, cli, status, error, expected_reason, passed
):
    calls = []
    monkeypatch.setattr(pilot, "prepare_stage", lambda unused: None)
    monkeypatch.setattr(
        pilot, "bounded_attach", lambda unused: (reason, cli, b"out", b"err")
    )

    def fake_docker(*args, **unused):
        calls.append(args)
        if args[0] == "inspect":
            return SimpleNamespace(
                stdout=json.dumps({
                    "ExitCode": exit_code, "OOMKilled": oom,
                    "Status": status, "Error": error,
                }),
                returncode=0,
            )
        return SimpleNamespace(stdout="", returncode=0)

    monkeypatch.setattr(pilot, "docker", fake_docker)
    result = pilot.run_pilot(Path("/run/qaos-worker-broker/staging/request-abcdefgh"))
    assert result["fixture"] == "python-single"
    assert result["expected_pass"] is passed
    assert result["reason"] == expected_reason
    assert "daemon failure secret" not in json.dumps(result)
    assert result["spec_sha256"] == pilot.PILOT_SPEC_SHA256
    assert result["stdout_bytes"] == 3
    assert result["stdout_sha256"] == hashlib.sha256(b"out").hexdigest()
    assert result["stderr_sha256"] == hashlib.sha256(b"err").hexdigest()
    assert [item[0] for item in calls] == ["create", "inspect", "rm"]
    assert calls[-1][1] == "-f"


def test_create_error_still_attempts_removal(monkeypatch):
    calls = []
    monkeypatch.setattr(pilot, "prepare_stage", lambda unused: None)

    def fake_docker(*args, **unused):
        calls.append(args[0])
        if args[0] == "create":
            raise OSError("create response lost")
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(pilot, "docker", fake_docker)
    with pytest.raises(OSError, match="response lost"):
        pilot.run_pilot(Path("/run/qaos-worker-broker/staging/request-abcdefgh"))
    assert calls == ["create", "rm"]


def test_create_error_and_failed_removal_report_cleanup_uncertainty(monkeypatch):
    calls = []
    monkeypatch.setattr(pilot, "prepare_stage", lambda unused: None)

    def fake_docker(*args, **unused):
        calls.append(args[0])
        if args[0] == "create":
            raise OSError("create response lost")
        return SimpleNamespace(returncode=1)

    monkeypatch.setattr(pilot, "docker", fake_docker)
    with pytest.raises(RuntimeError, match="cleanup is unverified"):
        pilot.run_pilot(Path("/run/qaos-worker-broker/staging/request-abcdefgh"))
    assert calls == ["create", "rm"]
