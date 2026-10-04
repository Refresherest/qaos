#!/usr/bin/env python3
"""Root-owned broker for the restricted QAOS worker exchange.

The synthetic harmless route remains the default. A separately pinned pilot
launcher can be enabled explicitly for one fixed Python acceptance fixture.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

try:
    import fcntl
except ModuleNotFoundError:  # pragma: no cover - worker is Linux
    fcntl = None

from qaos_worker_exchange import (
    PROTOCOL, VERSION, ProtocolError, canonical_json, decode_request, encode_frame,
)

LAUNCHER_SHA256 = "0bc39f9ab6eb917b0983ee3fab9dae79cf7c97f0103d654b30f33ad6fb89828e"
IMAGE_DIGEST = "python@sha256:b64631e04e4920160c50fbe8d8df828f7f35f06f425cb44aa09bca53e708a35a"
POLICY_ID = "qaos.synthetic.transport.harmless.v1"
RUNTIME_VERSION = "gvisor-20260831.0"
RESPONSE_LIMIT = 2250 * 1024
LAUNCHER_OUTPUT_LIMIT = 2 * 1024 * 1024
PILOT_POLICY_ID = "qaos.python-single.v1"
PILOT_LAUNCHER_PATH = Path("/usr/local/sbin/qaos-worker-pilot-launcher")
PILOT_ENABLE_PATH = Path("/etc/qaos-worker/enable-python-single-v1")
PILOT_ENABLE_BYTES = b"qaos.python-single.v1\n"
PILOT_LAUNCHER_SHA256 = "1b8e20cbc63999244862544f5c9933fb14cf9701d22b455bb753d4ebf4a81403"
PILOT_SPEC_SHA256 = "6aca4382c76e69fab92ec607eae303ae90bd408a11286a950228510a7d54d1a0"
PILOT_FILE_LIMIT = 64 * 1024
PILOT_PATHS = ("acceptance/acceptance.py", "candidate/candidate.py")
SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")


@dataclass(frozen=True)
class BrokerConfig:
    launcher: Path = Path("/usr/local/sbin/qaos-worker-launcher")
    replay_root: Path = Path("/var/lib/qaos-worker-broker/replay")
    staging_root: Path = Path("/run/qaos-worker-broker/staging")
    lock_path: Path = Path("/run/qaos-worker-broker/active.lock")
    worker_instance_id: str = "qaos-worker"
    expected_runtime: dict | None = None
    pilot_launcher: Path | None = None
    expected_pilot_runtime: dict | None = None
    pilot_spec_sha256: str | None = None

    def runtime(self):
        return self.expected_runtime or {
            "launcher_sha256": LAUNCHER_SHA256,
            "image_digest": IMAGE_DIGEST,
            "policy_id": POLICY_ID,
        }

    def allowed_runtimes(self):
        if self.expected_pilot_runtime is None:
            return self.runtime()
        if (self.pilot_launcher is None
                or self.pilot_launcher != PILOT_LAUNCHER_PATH
                or self.expected_pilot_runtime.get("policy_id") != PILOT_POLICY_ID
                or not isinstance(self.pilot_spec_sha256, str)
                or not SHA256_RE.fullmatch(self.pilot_spec_sha256)):
            raise RuntimeError("pilot runtime is not fully pinned")
        return (self.runtime(), self.expected_pilot_runtime)


def verify_pilot_enable_metadata(path):
    """A root-only fixed control file is the sole installed pilot switch."""
    for directory in reversed(path.parents):
        info = directory.lstat()
        if (not stat.S_ISDIR(info.st_mode) or info.st_uid != 0
                or stat.S_IMODE(info.st_mode) & 0o022):
            raise RuntimeError("pilot enable directory is not root-owned and fixed")
    info = path.lstat()
    if (not stat.S_ISREG(info.st_mode) or info.st_uid != 0
            or info.st_nlink != 1 or stat.S_IMODE(info.st_mode) != 0o400):
        raise RuntimeError("pilot enable file is not root-owned and private")


def installed_config(control_path=PILOT_ENABLE_PATH):
    """Retain the synthetic default unless the exact trusted switch exists."""
    try:
        control_path.lstat()
    except FileNotFoundError:
        return BrokerConfig()
    except OSError as error:
        raise RuntimeError("pilot enable file metadata unavailable") from error
    try:
        verify_pilot_enable_metadata(control_path)
        if control_path.read_bytes() != PILOT_ENABLE_BYTES:
            raise RuntimeError("pilot enable file contents are invalid")
    except OSError as error:
        raise RuntimeError("pilot enable file unavailable") from error
    return BrokerConfig(
        pilot_launcher=PILOT_LAUNCHER_PATH,
        expected_pilot_runtime={
            "launcher_sha256": PILOT_LAUNCHER_SHA256,
            "image_digest": IMAGE_DIGEST,
            "policy_id": PILOT_POLICY_ID,
        },
        pilot_spec_sha256=PILOT_SPEC_SHA256,
    )


class CleanupError(RuntimeError):
    pass


class RuntimeFailure(ProtocolError):
    pass


class PolicyFailure(ProtocolError):
    pass


def utc_second(now=None):
    return (now or datetime.now(timezone.utc)).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_bytes(value):
    return hashlib.sha256(value).hexdigest()


def ensure_private_directory(path):
    path.mkdir(parents=True, exist_ok=True, mode=0o700)
    path.chmod(0o700)


def acquire_lock(config):
    if fcntl is None:
        raise RuntimeError("broker file locking requires Linux")
    ensure_private_directory(config.lock_path.parent)
    lock = config.lock_path.open("a+")
    os.chmod(config.lock_path, 0o600)
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError as error:
        lock.close()
        raise ProtocolError("another broker request is active") from error
    return lock


def claim_replay(request, config):
    marker = config.replay_root / request["request_id"]
    record = canonical_json({
        "nonce_sha256": sha256_bytes(request["nonce"].encode("ascii")),
        "request_sha256": sha256_bytes(canonical_json(request)),
    })
    try:
        ensure_private_directory(config.replay_root)
        descriptor = os.open(marker, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(record)
            stream.flush()
            os.fsync(stream.fileno())
        fsync_directory(config.replay_root)
    except FileExistsError as error:
        raise PolicyFailure("request replay rejected") from error
    except OSError as error:
        raise RuntimeFailure("replay storage failed") from error
    return marker


def fsync_directory(path):
    directory = os.open(path, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(directory)
    finally:
        os.close(directory)


def stage_members(request, payloads, config):
    root = None
    try:
        ensure_private_directory(config.staging_root)
        root = Path(tempfile.mkdtemp(prefix="request-", dir=config.staging_root))
        root.chmod(0o700)
        pilot = request["runtime"]["policy_id"] == PILOT_POLICY_ID
        for member, payload in zip(request["members"], payloads, strict=True):
            write_member(root, member, payload, pilot=pilot)
        return root
    except Exception as original:
        if root is not None:
            try:
                cleanup_staging(root)
            except Exception as error:
                raise CleanupError("partial staging cleanup failed") from error
        raise RuntimeFailure("staging failed") from original


def write_member(root, member, payload, *, pilot=False):
    target = root / member["path"] if pilot else root / member["role"] / member["path"]
    target.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    target.parent.chmod(0o700)
    descriptor = os.open(
        target, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o400
    )
    with os.fdopen(descriptor, "wb") as stream:
        stream.write(payload)
        stream.flush()
        os.fsync(stream.fileno())
    if target.read_bytes() != payload:
        raise ProtocolError("staged member verification failed")


def cleanup_staging(root):
    def make_removable(function, path, error):
        os.chmod(path, 0o700)
        function(path)
    shutil.rmtree(root, onexc=make_removable)


def verify_pilot_launcher_metadata(path):
    """Refuse mutable or linked installed paths before hashing/executing."""
    try:
        for directory in reversed(path.parents):
            info = directory.lstat()
            if (not stat.S_ISDIR(info.st_mode) or info.st_uid != 0
                    or stat.S_IMODE(info.st_mode) & 0o022):
                raise RuntimeFailure("pilot launcher directory is not root-owned and fixed")
        info = path.lstat()
        if (not stat.S_ISREG(info.st_mode) or info.st_uid != 0
                or info.st_nlink != 1
                or stat.S_IMODE(info.st_mode) & 0o022
                or not stat.S_IMODE(info.st_mode) & 0o111):
            raise RuntimeFailure("pilot launcher path is not root-owned and fixed")
    except OSError as error:
        raise RuntimeFailure("pilot launcher metadata unavailable") from error


def verify_launcher(config, pilot=False):
    launcher = config.pilot_launcher if pilot else config.launcher
    digest = (config.expected_pilot_runtime["launcher_sha256"]
              if pilot else config.runtime()["launcher_sha256"])
    if pilot:
        if launcher != PILOT_LAUNCHER_PATH:
            raise RuntimeFailure("pilot launcher path is not pinned")
        verify_pilot_launcher_metadata(launcher)
    try:
        value = launcher.read_bytes()
    except OSError as error:
        raise RuntimeFailure("trusted launcher unavailable") from error
    if sha256_bytes(value) != digest:
        raise RuntimeFailure("trusted launcher digest mismatch")


def validate_pilot_request(request, payloads):
    members = request["members"]
    if (len(members) != 2
            or [(m["role"], m["path"]) for m in members] != [
                ("acceptance", PILOT_PATHS[0]), ("candidate", PILOT_PATHS[1])
            ]):
        raise ProtocolError("pilot requires two exact fixed members")
    if request["candidate_artifact"]["artifact_id"] == request["acceptance_artifact"]["artifact_id"]:
        raise ProtocolError("pilot Artifact identities must differ")
    for member, payload in zip(members, payloads, strict=True):
        if not 0 < len(payload) <= PILOT_FILE_LIMIT:
            raise ProtocolError("pilot member exceeds fixed bounds")
        if request[f'{member["role"]}_artifact']["content_sha256"] != member["sha256"]:
            raise ProtocolError("pilot Artifact digest does not match member")
        try:
            payload.decode("utf-8", "strict")
        except UnicodeDecodeError as error:
            raise ProtocolError("pilot member must be UTF-8") from error


def run_pilot(config, staging):
    started = time.monotonic()
    try:
        result = subprocess.run(
            [str(config.pilot_launcher), "python-single", str(staging)],
            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, timeout=90, check=False,
        )
    except OSError as error:
        raise RuntimeFailure("trusted pilot launcher failed") from error
    except subprocess.TimeoutExpired as error:
        raise CleanupError("pilot launcher timed out; cleanup is unverified") from error
    if len(result.stdout) > LAUNCHER_OUTPUT_LIMIT or len(result.stderr) > LAUNCHER_OUTPUT_LIMIT:
        raise CleanupError("pilot launcher output exceeded limit; cleanup is unverified")
    try:
        evidence = json.loads(result.stdout.decode("utf-8", "strict"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise CleanupError("pilot launcher returned no trusted cleanup evidence") from error
    if (not isinstance(evidence, dict)
            or evidence.get("fixture") != "python-single"
            or evidence.get("image") != config.expected_pilot_runtime["image_digest"]
            or evidence.get("spec_sha256") != config.pilot_spec_sha256
            or type(evidence.get("expected_pass")) is not bool
            or result.returncode != (0 if evidence["expected_pass"] else 1)):
        raise CleanupError("pilot launcher evidence mismatch; cleanup is unverified")
    for name in ("stdout", "stderr"):
        count, digest, preview = (
            evidence.get(f"{name}_bytes"), evidence.get(f"{name}_sha256"),
            evidence.get(f"{name}_preview"),
        )
        if (type(count) is not int or not 0 <= count <= 1024 * 1024
                or not isinstance(digest, str) or not SHA256_RE.fullmatch(digest)
                or not isinstance(preview, str)
                or len(preview.encode("utf-8")) > 480):
            raise CleanupError("pilot launcher stream evidence invalid; cleanup is unverified")
    if (type(evidence.get("exit_code")) is not int
            or type(evidence.get("docker_cli_exit")) is not int
            or type(evidence.get("oom_killed")) is not bool
            or evidence.get("reason") not in {
                "completion", "deadline", "stdout_limit", "stderr_limit", "oom",
                "runtime_error",
            }):
        raise CleanupError("pilot launcher execution evidence invalid; cleanup is unverified")
    observed_pass = (
        evidence["reason"] == "completion"
        and evidence["docker_cli_exit"] == 0
        and evidence["exit_code"] == 0
        and evidence["oom_killed"] is False
    )
    if (evidence["expected_pass"] is not observed_pass
            or (evidence["reason"] == "oom") is not evidence["oom_killed"]):
        raise CleanupError("pilot launcher pass evidence inconsistent; cleanup is unverified")
    return evidence, int((time.monotonic() - started) * 1000)


def run_harmless(config):
    started = time.monotonic()
    try:
        result = subprocess.run(
            [str(config.launcher), "harmless"], stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=45, check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise RuntimeFailure("trusted launcher failed") from error
    if len(result.stdout) > LAUNCHER_OUTPUT_LIMIT or len(result.stderr) > LAUNCHER_OUTPUT_LIMIT:
        raise RuntimeFailure("trusted launcher output exceeded limit")
    try:
        evidence = json.loads(result.stdout.decode("utf-8", "strict"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RuntimeFailure("trusted launcher returned invalid evidence") from error
    if result.returncode != 0 or evidence.get("fixture") != "harmless" or not evidence.get("expected_pass"):
        raise RuntimeFailure("trusted harmless fixture did not pass")
    return evidence, int((time.monotonic() - started) * 1000)


def stream_evidence(byte_count, digest, preview, *, truncated=False):
    return {"bytes": byte_count, "sha256": digest, "truncated": truncated, "text_preview": preview}


def build_response(request, evidence, duration_ms, config, started_at, cleanup,
                   outcome="completed", termination_reason=None):
    pilot = request["runtime"].get("policy_id") == PILOT_POLICY_ID
    empty_digest = sha256_bytes(b"")
    evidence = evidence or {
        "exit_code": None, "oom_killed": False, "reason": termination_reason,
        "stdout_bytes": 0, "stdout_sha256": empty_digest, "stdout_preview": "",
        "stderr_bytes": 0, "stderr_sha256": empty_digest, "stderr_preview": "",
        "spec_sha256": None,
    }
    response = {
        "protocol": PROTOCOL, "version": VERSION,
        "request_id": request["request_id"], "nonce": request["nonce"],
        "objective_id": request["objective_id"], "task_id": request["task_id"],
        "candidate_artifact": request["candidate_artifact"],
        "acceptance_artifact": request["acceptance_artifact"],
        "worker_instance_id": config.worker_instance_id,
        "launcher_sha256": request["runtime"]["launcher_sha256"],
        "runtime_version": RUNTIME_VERSION,
        "image_digest": request["runtime"]["image_digest"],
        "policy_id": request["runtime"]["policy_id"],
        "started_at": started_at, "completed_at": utc_second(),
        "outcome": outcome, "exit_code": evidence["exit_code"],
        "oom_killed": evidence["oom_killed"], "termination_reason": termination_reason or evidence["reason"],
        "stdout": stream_evidence(evidence["stdout_bytes"], evidence["stdout_sha256"], evidence["stdout_preview"], truncated=pilot and evidence["reason"] in {"deadline", "stdout_limit", "stderr_limit", "oom"}),
        "stderr": stream_evidence(evidence["stderr_bytes"], evidence["stderr_sha256"], evidence["stderr_preview"], truncated=pilot and evidence["reason"] in {"deadline", "stdout_limit", "stderr_limit", "oom"}),
        "resource_evidence": {
            "fixture": ("python-single" if pilot else "harmless")
            if evidence["spec_sha256"] else None,
            "spec_sha256": evidence["spec_sha256"],
        },
        "acceptance_results": ([{
            "test_id": "pilot.python-single.acceptance" if pilot else "transport.synthetic.harmless",
            "status": "passed" if outcome == "completed" else "failed",
            "duration_ms": duration_ms,
        }] if evidence["spec_sha256"] and outcome in {"completed", "candidate_failed"} else []),
        "cleanup": cleanup,
    }
    response["response_sha256"] = sha256_bytes(canonical_json(response))
    return response


def process(stream_in, stream_out, config=None, now=None):
    config = config or BrokerConfig()
    staging = None
    with acquire_lock(config):
        request, payloads = decode_request(stream_in, config.allowed_runtimes(), now)
        pilot = request["runtime"].get("policy_id") == PILOT_POLICY_ID
        if pilot:
            validate_pilot_request(request, payloads)
        started_at = utc_second(now)
        outcome = "completed"
        reason = None
        evidence = None
        duration_ms = 0
        cleanup = {"staging_removed": True, "launcher_cleanup_reported": False}
        try:
            claim_replay(request, config)
            try:
                staging = stage_members(request, payloads, config)
                verify_launcher(config, pilot)
                if pilot:
                    evidence, duration_ms = run_pilot(config, staging)
                    if not evidence["expected_pass"]:
                        outcome = (
                            "candidate_failed"
                            if evidence["reason"] == "completion"
                            and evidence["exit_code"] != 0
                            else "limit_terminated"
                            if evidence["reason"] in {
                                "deadline", "stdout_limit", "stderr_limit", "oom"
                            }
                            else "runtime_failed"
                        )
                else:
                    evidence, duration_ms = run_harmless(config)
                cleanup["launcher_cleanup_reported"] = True
            except Exception as error:
                if isinstance(error, CleanupError):
                    outcome = "cleanup_failed"
                else:
                    outcome = "runtime_failed" if isinstance(error, RuntimeFailure) else "policy_rejected"
                reason = "runtime_refused" if outcome == "runtime_failed" else "policy_refused"
                if outcome == "cleanup_failed":
                    reason = "cleanup_failed"
                    cleanup["staging_removed"] = False
        except PolicyFailure:
            outcome = "policy_rejected"
            reason = "replay_refused"
        except RuntimeFailure:
            outcome = "runtime_failed"
            reason = "replay_storage_failed"
        try:
            if not (outcome == "cleanup_failed" and staging is None):
                if staging is not None:
                    cleanup_staging(staging)
                cleanup["staging_removed"] = staging is None or not staging.exists()
        except Exception:
            cleanup["staging_removed"] = False
            outcome = "cleanup_failed"
            reason = "cleanup_failed"
        response = canonical_json(build_response(
            request, evidence, duration_ms, config, started_at, cleanup, outcome, reason
        ))
        stream_out.write(encode_frame(response, RESPONSE_LIMIT))
        stream_out.flush()


def main():
    if os.geteuid() != 0:
        return 2
    try:
        process(sys.stdin.buffer, sys.stdout.buffer, installed_config())
    except Exception:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
