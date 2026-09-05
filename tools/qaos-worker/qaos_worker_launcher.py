#!/usr/bin/env python3
"""Fixed, root-operated launcher for bounded QAOS worker validation fixtures.

This is infrastructure test tooling. It does not accept source paths, commands,
images, mounts, environment variables, Docker flags, or other candidate input.
"""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import selectors
import subprocess
import sys
import time
import uuid
from dataclasses import dataclass
from pathlib import Path


IMAGE = "python@sha256:b64631e04e4920160c50fbe8d8df828f7f35f06f425cb44aa09bca53e708a35a"
OUTPUT_LIMIT = 1024 * 1024
DEADLINE_SECONDS = 30
KILL_GRACE_SECONDS = 5
NAME_PREFIX = "qaos-negative-"
LOCK_PATH = Path("/run/qaos-worker-launcher.lock")


@dataclass(frozen=True)
class Fixture:
    argv: tuple[str, ...]
    expected: str
    expected_stdout: str | None = None


FIXTURES = {
    "harmless": Fixture(
        ("python", "-c", "print('QAOS_HARMLESS_OK')"),
        "success",
        "QAOS_HARMLESS_OK\n",
    ),
    "filesystem": Fixture(
        (
            "python",
            "-c",
            """from pathlib import Path
assert not Path('/opt/qaos-worker/host-canary').exists()
try:
    Path('/root-write-should-fail').write_text('x')
except OSError:
    pass
else:
    raise SystemExit(91)
Path('/tmp/fixture-write').write_text('x')
print('FILESYSTEM_LIMIT_OK')
""",
        ),
        "success",
        "FILESYSTEM_LIMIT_OK\n",
    ),
    "network": Fixture(
        (
            "python",
            "-c",
            """import socket
for host, port in [('example.com', 80), ('169.254.169.254', 80)]:
    try:
        connection = socket.create_connection((host, port), 2)
    except OSError:
        continue
    connection.close()
    raise SystemExit(93)
print('NETWORK_LIMIT_OK')
""",
        ),
        "success",
        "NETWORK_LIMIT_OK\n",
    ),
    "memory": Fixture(
        (
            "python",
            "-c",
            "payload = bytearray(1100 * 1024 * 1024); print(len(payload))",
        ),
        "oom",
    ),
    "pids": Fixture(
        (
            "python",
            "-c",
            """import subprocess
children = []
try:
    for _ in range(40):
        children.append(subprocess.Popen(['sleep', '10']))
except OSError:
    print('PIDS_LIMIT_OK')
else:
    raise SystemExit(94)
finally:
    for child in children:
        child.terminate()
    for child in children:
        try:
            child.wait(timeout=2)
        except subprocess.TimeoutExpired:
            child.kill()
""",
        ),
        "success",
        "PIDS_LIMIT_OK\n",
    ),
    "scratch": Fixture(
        (
            "python",
            "-c",
            """block = b'x' * (1024 * 1024)
try:
    with open('/tmp/fill', 'wb', buffering=0) as stream:
        for _ in range(257):
            stream.write(block)
except OSError:
    print('SCRATCH_LIMIT_OK')
else:
    raise SystemExit(95)
""",
        ),
        "success",
        "SCRATCH_LIMIT_OK\n",
    ),
    "output": Fixture(
        (
            "python",
            "-c",
            "import sys; sys.stdout.write('x' * (1024 * 1024 + 1)); sys.stdout.flush()",
        ),
        "stdout_limit",
    ),
    "deadline": Fixture(
        ("python", "-c", "import time; time.sleep(35)"), "deadline"
    ),
    "descendant": Fixture(
        (
            "python",
            "-c",
            "import subprocess,time; subprocess.Popen(['sleep','60']); time.sleep(35)",
        ),
        "deadline",
    ),
    "fake-success": Fixture(
        (
            "python",
            "-c",
            "import sys; print('{\"status\":\"PASS\"}'); sys.exit(7)",
        ),
        "candidate_failure",
    ),
}


def docker(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["/usr/bin/docker", *args],
        check=check,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=15,
    )


def container_args(name: str, fixture: Fixture) -> list[str]:
    return [
        "create",
        "--name",
        name,
        "--runtime=runsc",
        "--network=none",
        "--read-only",
        "--tmpfs",
        "/tmp:rw,noexec,nosuid,nodev,size=268435456",
        "--cpus=1",
        "--memory=1g",
        "--memory-swap=1g",
        "--pids-limit=32",
        "--cap-drop=ALL",
        "--security-opt=no-new-privileges",
        "--user=65534:65534",
        "--log-driver=none",
        IMAGE,
        *fixture.argv,
    ]


def bounded_attach(name: str) -> tuple[str, int, bytes, bytes]:
    process = subprocess.Popen(
        ["/usr/bin/docker", "start", "-a", name],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert process.stdout is not None and process.stderr is not None
    selector = selectors.DefaultSelector()
    selector.register(process.stdout, selectors.EVENT_READ, "stdout")
    selector.register(process.stderr, selectors.EVENT_READ, "stderr")
    buffers = {"stdout": bytearray(), "stderr": bytearray()}
    started = time.monotonic()
    reason = "completion"

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
            buffers[stream].extend(chunk[: max(remaining, 0)])
            if len(chunk) > remaining:
                reason = f"{stream}_limit"
                break
        if reason != "completion":
            break

    if reason != "completion":
        docker("kill", name, check=False)
    try:
        return_code = process.wait(timeout=KILL_GRACE_SECONDS)
    except subprocess.TimeoutExpired:
        process.kill()
        return_code = process.wait(timeout=2)
    return reason, return_code, bytes(buffers["stdout"]), bytes(buffers["stderr"])


def state_for(name: str) -> dict[str, object]:
    result = docker("inspect", name, "--format", "{{json .State}}")
    return json.loads(result.stdout)


def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def preview(value: bytes) -> str:
    return value[:160].decode("utf-8", "replace")


def expected_pass(fixture: Fixture, result: dict[str, object]) -> bool:
    stdout = result["stdout_preview"]
    if fixture.expected == "success":
        return (
            result["reason"] == "completion"
            and result["exit_code"] == 0
            and stdout == fixture.expected_stdout
        )
    if fixture.expected == "oom":
        return bool(result["oom_killed"]) and result["exit_code"] != 0
    if fixture.expected in {"stdout_limit", "deadline"}:
        return result["reason"] == fixture.expected
    if fixture.expected == "candidate_failure":
        return (
            result["reason"] == "completion"
            and result["exit_code"] == 7
            and '"status":"PASS"' in str(stdout)
        )
    return False


def run_fixture(fixture_name: str) -> dict[str, object]:
    if fixture_name not in FIXTURES:
        raise ValueError("fixture is not allowlisted")
    fixture = FIXTURES[fixture_name]
    name = NAME_PREFIX + uuid.uuid4().hex
    spec = container_args(name, fixture)
    created = False
    cleaned = False
    try:
        docker(*spec)
        created = True
        reason, cli_exit, stdout, stderr = bounded_attach(name)
        state = state_for(name)
        result: dict[str, object] = {
            "fixture": fixture_name,
            "image": IMAGE,
            "spec_sha256": hashlib.sha256(
                json.dumps(spec[3:], separators=(",", ":")).encode()
            ).hexdigest(),
            "reason": reason,
            "docker_cli_exit": cli_exit,
            "exit_code": state.get("ExitCode"),
            "oom_killed": state.get("OOMKilled"),
            "stdout_bytes": len(stdout),
            "stdout_sha256": digest(stdout),
            "stdout_preview": preview(stdout),
            "stderr_bytes": len(stderr),
            "stderr_sha256": digest(stderr),
            "stderr_preview": preview(stderr),
        }
        result["expected_pass"] = expected_pass(fixture, result)
        return result
    finally:
        if created:
            cleaned = docker("rm", "-f", name, check=False).returncode == 0
        if created and not cleaned:
            raise RuntimeError(f"failed to remove owned container {name}")


def acquire_lock():
    LOCK_PATH.touch(mode=0o600, exist_ok=True)
    lock = LOCK_PATH.open("r+")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError as error:
        raise RuntimeError("another QAOS worker fixture is active") from error
    return lock


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("fixture", choices=sorted(FIXTURES))
    args = parser.parse_args()
    if os.geteuid() != 0:
        parser.error("launcher must run as root")
    with acquire_lock():
        result = run_fixture(args.fixture)
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0 if result["expected_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
