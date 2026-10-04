#!/usr/bin/env python3
"""Fixed, root-operated launcher for one admitted Python pilot.

Only the reviewed broker supplies a private stage directory. The candidate and
acceptance files provide code bytes, never a command, image, mount, or Docker
option. This module is intentionally separate from the installed synthetic
launcher so its existing digest and behaviour remain unchanged.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import selectors
import stat
import subprocess
import sys
import time
import uuid
from pathlib import Path


IMAGE = "python@sha256:b64631e04e4920160c50fbe8d8df828f7f35f06f425cb44aa09bca53e708a35a"
STAGING_ROOT = Path("/run/qaos-worker-broker/staging")
LOCK_PATH = Path("/run/qaos-worker-launcher.lock")
NAME_PREFIX = "qaos-pilot-"
MAX_FILE_BYTES = 64 * 1024
OUTPUT_LIMIT = 1024 * 1024
DEADLINE_SECONDS = 30
KILL_GRACE_SECONDS = 5
STAGE_NAME = re.compile(r"request-[a-z0-9_]{8}\Z")
SOURCE_PATHS = (
    "candidate/candidate.py",
    "acceptance/acceptance.py",
)
CONTAINER_CANDIDATE = "/opt/qaos/candidate/candidate.py"
CONTAINER_ACCEPTANCE = "/opt/qaos/acceptance/acceptance.py"
COMMAND = (
    "python", "-I", "-S", "-B", CONTAINER_ACCEPTANCE, CONTAINER_CANDIDATE,
)


def container_args(name: str, stage_root: str) -> list[str]:
    """Return the entire fixed Docker create command after /usr/bin/docker."""
    mounts = [
        "type=bind,src=" + stage_root + "/" + SOURCE_PATHS[0]
        + ",dst=" + CONTAINER_CANDIDATE + ",readonly",
        "type=bind,src=" + stage_root + "/" + SOURCE_PATHS[1]
        + ",dst=" + CONTAINER_ACCEPTANCE + ",readonly",
    ]
    return [
        "create", "--name", name,
        "--pull=never", "--runtime=runsc", "--network=none", "--read-only",
        "--tmpfs", "/tmp:rw,noexec,nosuid,nodev,size=268435456",
        "--cpus=1", "--memory=1g", "--memory-swap=1g", "--pids-limit=32",
        "--cap-drop=ALL", "--security-opt=no-new-privileges",
        "--user=65534:65534", "--log-driver=none",
        "--mount", mounts[0], "--mount", mounts[1],
        IMAGE, *COMMAND,
    ]


def _canonical_spec_digest() -> str:
    # Omit the random container name and normalize the private request path.
    fixed = container_args("<name>", "<stage>")
    return hashlib.sha256(
        json.dumps(fixed[3:], separators=(",", ":")).encode("utf-8")
    ).hexdigest()


PILOT_SPEC_SHA256 = _canonical_spec_digest()


def _check_directory(path: Path, *, private: bool) -> None:
    info = path.lstat()
    if not stat.S_ISDIR(info.st_mode) or info.st_uid != 0:
        raise ValueError("stage directory must be root-owned and not a symlink")
    mode = stat.S_IMODE(info.st_mode)
    if (private and mode != 0o700) or (not private and mode & 0o022):
        raise ValueError("stage directory permissions are unsafe")


def _check_entries(path: Path, expected: set[str]) -> None:
    if set(os.listdir(path)) != expected:
        raise ValueError("stage contains unexpected entries")


def _open_source(path: Path) -> int:
    if not hasattr(os, "O_NOFOLLOW"):
        raise RuntimeError("pilot launcher requires Linux no-follow file opens")
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
    try:
        info = os.fstat(descriptor)
        if (not stat.S_ISREG(info.st_mode) or info.st_uid != 0
                or info.st_nlink != 1 or stat.S_IMODE(info.st_mode) != 0o400):
            raise ValueError("stage source ownership or mode is unsafe")
        if not 0 < info.st_size <= MAX_FILE_BYTES:
            raise ValueError("stage source size is outside pilot bounds")
        source = bytearray()
        while len(source) < info.st_size:
            chunk = os.read(descriptor, info.st_size - len(source))
            if not chunk:
                raise ValueError("stage source changed during validation")
            source.extend(chunk)
        if os.read(descriptor, 1) or os.fstat(descriptor).st_size != info.st_size:
            raise ValueError("stage source changed during validation")
        _validate_source_bytes(source)
        return descriptor
    except BaseException:
        os.close(descriptor)
        raise


def _validate_source_bytes(source: bytes) -> None:
    if not 0 < len(source) <= MAX_FILE_BYTES:
        raise ValueError("stage source size is outside pilot bounds")
    try:
        source.decode("utf-8", "strict")
    except UnicodeDecodeError as error:
        raise ValueError("stage source is not UTF-8") from error


def prepare_stage(stage_root: Path, *, staging_root: Path = STAGING_ROOT) -> None:
    """Check the exact broker tree, then make only its two files mount-readable."""
    if (not stage_root.is_absolute() or ".." in stage_root.parts
            or stage_root.parent != staging_root
            or not STAGE_NAME.fullmatch(stage_root.name)):
        raise ValueError("stage root is outside the fixed broker staging location")
    if staging_root == STAGING_ROOT:
        _check_directory(Path("/run"), private=False)
    _check_directory(staging_root.parent, private=True)
    _check_directory(staging_root, private=True)
    _check_directory(stage_root, private=True)
    _check_entries(stage_root, {"candidate", "acceptance"})
    for role in ("candidate", "acceptance"):
        _check_directory(stage_root / role, private=True)
        _check_entries(stage_root / role, {role + ".py"})

    descriptors = []
    try:
        for relative in SOURCE_PATHS:
            descriptors.append(_open_source(stage_root / relative))
        # The host tree remains private (0700); only the two already-validated
        # files become readable by the container's unprivileged UID.
        for descriptor in descriptors:
            os.fchmod(descriptor, 0o444)
    finally:
        for descriptor in descriptors:
            os.close(descriptor)


def docker(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["/usr/bin/docker", *args], check=check, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=15,
    )


def bounded_attach(name: str) -> tuple[str, int, bytes, bytes]:
    process = subprocess.Popen(
        ["/usr/bin/docker", "start", "-a", name],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    assert process.stdout is not None and process.stderr is not None
    selector = selectors.DefaultSelector()
    selector.register(process.stdout, selectors.EVENT_READ, "stdout")
    selector.register(process.stderr, selectors.EVENT_READ, "stderr")
    buffers = {"stdout": bytearray(), "stderr": bytearray()}
    started = time.monotonic()
    reason = "completion"
    try:
        while selector.get_map():
            if time.monotonic() - started >= DEADLINE_SECONDS:
                reason = "deadline"
                break
            for key, _ in selector.select(timeout=0.1):
                chunk = os.read(key.fileobj.fileno(), 65536)
                if not chunk:
                    selector.unregister(key.fileobj)
                    continue
                stream = key.data
                remaining = OUTPUT_LIMIT - len(buffers[stream])
                buffers[stream].extend(chunk[:max(remaining, 0)])
                if len(chunk) > remaining:
                    reason = f"{stream}_limit"
                    break
            if reason != "completion":
                break
    except BaseException:
        try:
            docker("kill", name, check=False)
        finally:
            if process.poll() is None:
                process.kill()
            process.wait(timeout=2)
        raise
    finally:
        selector.close()
    if reason != "completion":
        docker("kill", name, check=False)
    try:
        cli_exit = process.wait(timeout=KILL_GRACE_SECONDS)
    except subprocess.TimeoutExpired:
        process.kill()
        cli_exit = process.wait(timeout=2)
    process.stdout.close()
    process.stderr.close()
    return reason, cli_exit, bytes(buffers["stdout"]), bytes(buffers["stderr"])


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _preview(data: bytes) -> str:
    return data[:160].decode("utf-8", "replace")


def run_pilot(stage_root: Path) -> dict[str, object]:
    prepare_stage(stage_root)
    name = NAME_PREFIX + uuid.uuid4().hex
    create_attempted = False
    try:
        create_attempted = True
        docker(*container_args(name, stage_root.as_posix()))
        reason, cli_exit, stdout, stderr = bounded_attach(name)
        state = json.loads(docker("inspect", name, "--format", "{{json .State}}").stdout)
        if reason == "completion":
            if state.get("OOMKilled") is True:
                reason = "oom"
            elif (state.get("Status") != "exited" or state.get("Error") != ""
                  or type(cli_exit) is not int
                  or type(state.get("ExitCode")) is not int
                  or cli_exit != state["ExitCode"]):
                reason = "runtime_error"
        result: dict[str, object] = {
            "fixture": "python-single", "image": IMAGE,
            "spec_sha256": PILOT_SPEC_SHA256,
            "reason": reason, "docker_cli_exit": cli_exit,
            "exit_code": state.get("ExitCode"), "oom_killed": state.get("OOMKilled"),
            "stdout_bytes": len(stdout), "stdout_sha256": _digest(stdout),
            "stdout_preview": _preview(stdout),
            "stderr_bytes": len(stderr), "stderr_sha256": _digest(stderr),
            "stderr_preview": _preview(stderr),
        }
        result["expected_pass"] = (
            reason == "completion" and cli_exit == 0
            and state.get("ExitCode") == 0 and state.get("OOMKilled") is False
        )
        return result
    finally:
        if create_attempted:
            try:
                removed = docker("rm", "-f", name, check=False).returncode == 0
            except Exception as error:
                raise RuntimeError("pilot container cleanup is unverified") from error
            if not removed:
                raise RuntimeError("pilot container cleanup is unverified")


def acquire_lock():
    try:
        import fcntl
    except ModuleNotFoundError as error:  # pragma: no cover - worker is Linux
        raise RuntimeError("pilot launcher requires Linux locking") from error
    LOCK_PATH.touch(mode=0o600, exist_ok=True)
    lock = LOCK_PATH.open("r+")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError as error:
        lock.close()
        raise RuntimeError("another QAOS worker fixture is active") from error
    return lock


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("fixture", choices=["python-single"])
    parser.add_argument("stage_root")
    args = parser.parse_args()
    if os.geteuid() != 0:
        parser.error("pilot launcher must run as root")
    with acquire_lock():
        result = run_pilot(Path(args.stage_root))
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0 if result["expected_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
