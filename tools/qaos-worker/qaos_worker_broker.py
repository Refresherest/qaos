#!/usr/bin/env python3
"""Root-owned synthetic broker for the restricted QAOS worker exchange.

This stage validates and stages bounded synthetic members, then invokes only the
reviewed fixed ``harmless`` launcher fixture. Staged members are never executed.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
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


@dataclass(frozen=True)
class BrokerConfig:
    launcher: Path = Path("/usr/local/sbin/qaos-worker-launcher")
    replay_root: Path = Path("/var/lib/qaos-worker-broker/replay")
    staging_root: Path = Path("/run/qaos-worker-broker/staging")
    lock_path: Path = Path("/run/qaos-worker-broker/active.lock")
    worker_instance_id: str = "qaos-worker"
    expected_runtime: dict | None = None

    def runtime(self):
        return self.expected_runtime or {
            "launcher_sha256": LAUNCHER_SHA256,
            "image_digest": IMAGE_DIGEST,
            "policy_id": POLICY_ID,
        }


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
        for member, payload in zip(request["members"], payloads, strict=True):
            write_member(root, member, payload)
        return root
    except Exception as original:
        if root is not None:
            try:
                cleanup_staging(root)
            except Exception as error:
                raise CleanupError("partial staging cleanup failed") from error
        raise RuntimeFailure("staging failed") from original


def write_member(root, member, payload):
    target = root / member["role"] / member["path"]
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


def verify_launcher(config):
    try:
        value = config.launcher.read_bytes()
    except OSError as error:
        raise RuntimeFailure("trusted launcher unavailable") from error
    if sha256_bytes(value) != config.runtime()["launcher_sha256"]:
        raise RuntimeFailure("trusted launcher digest mismatch")


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


def stream_evidence(byte_count, digest, preview):
    return {"bytes": byte_count, "sha256": digest, "truncated": False, "text_preview": preview}


def build_response(request, evidence, duration_ms, config, started_at, cleanup,
                   outcome="completed", termination_reason=None):
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
        "launcher_sha256": config.runtime()["launcher_sha256"],
        "runtime_version": RUNTIME_VERSION,
        "image_digest": config.runtime()["image_digest"],
        "policy_id": config.runtime()["policy_id"],
        "started_at": started_at, "completed_at": utc_second(),
        "outcome": outcome, "exit_code": evidence["exit_code"],
        "oom_killed": evidence["oom_killed"], "termination_reason": termination_reason or evidence["reason"],
        "stdout": stream_evidence(evidence["stdout_bytes"], evidence["stdout_sha256"], evidence["stdout_preview"]),
        "stderr": stream_evidence(evidence["stderr_bytes"], evidence["stderr_sha256"], evidence["stderr_preview"]),
        "resource_evidence": {"fixture": "harmless" if evidence["spec_sha256"] else None, "spec_sha256": evidence["spec_sha256"]},
        "acceptance_results": ([{"test_id": "transport.synthetic.harmless", "status": "passed", "duration_ms": duration_ms}] if outcome == "completed" else []),
        "cleanup": cleanup,
    }
    response["response_sha256"] = sha256_bytes(canonical_json(response))
    return response


def process(stream_in, stream_out, config=None, now=None):
    config = config or BrokerConfig()
    staging = None
    with acquire_lock(config):
        request, payloads = decode_request(stream_in, config.runtime(), now)
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
                verify_launcher(config)
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
        process(sys.stdin.buffer, sys.stdout.buffer)
    except Exception:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
