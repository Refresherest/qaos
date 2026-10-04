#!/usr/bin/env python3
"""Targeted, rollback-armed deployment of the fixed worker pilot route.

This is a local reviewed artifact until a separate live work order authorizes
staging or invocation on qaos-worker. It changes only the pinned broker,
protocol, pilot launcher and enablement control; it never changes SSH, sudoers,
identities, the synthetic launcher or QAOS product data.
"""

from __future__ import annotations

import hashlib
import os
import stat
import subprocess
import sys
import tempfile
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


OLD_BROKER_SHA256 = "d0432efc08309eaa41e9e09e741c43da22582dcf6ab43e18796fbfe6588c157d"
NEW_BROKER_SHA256 = "416fd9090ea0aaf8bd42d33c9fbef2c6f1fe2396b8e158ae2dd3353deedde7f7"
OLD_EXCHANGE_SHA256 = "5b1357f3e79c4ea6e3519c7e265b2ba8c7301750ef0530f7f538bd5b86b5c79c"
NEW_EXCHANGE_SHA256 = "682f9545defd4b430927666ce69d334a9fac066a475b56b458cc43c2cdea0026"
PILOT_LAUNCHER_SHA256 = "1b8e20cbc63999244862544f5c9933fb14cf9701d22b455bb753d4ebf4a81403"
ENABLE_BYTES = b"qaos.python-single.v1\n"
CREATED_DIRECTORY_BYTES = b"created-enable-directory\n"
TIMER_UNIT = "qaos-worker-pilot-rollback"
LOCK_PATH = Path("/run/qaos-worker-pilot-deploy.lock")


@dataclass(frozen=True)
class Layout:
    stage: Path
    state: Path
    broker: Path
    exchange: Path
    pilot_launcher: Path
    enable: Path

    @classmethod
    def production(cls) -> Layout:
        return cls(
            stage=Path("/var/lib/qaos-worker-pilot-stage"),
            state=Path("/var/lib/qaos-worker-pilot-upgrade"),
            broker=Path("/usr/local/sbin/qaos-worker-broker"),
            exchange=Path("/usr/local/sbin/qaos_worker_exchange.py"),
            pilot_launcher=Path("/usr/local/sbin/qaos-worker-pilot-launcher"),
            enable=Path("/etc/qaos-worker/enable-python-single-v1"),
        )

    @property
    def staged_broker(self) -> Path:
        return self.stage / "qaos_worker_broker.py"

    @property
    def staged_launcher(self) -> Path:
        return self.stage / "qaos_worker_pilot_launcher.py"

    @property
    def staged_exchange(self) -> Path:
        return self.stage / "qaos_worker_exchange.py"

    @property
    def staged_deploy(self) -> Path:
        return self.stage / "qaos_worker_pilot_deploy.py"

    @property
    def broker_backup(self) -> Path:
        return self.state / "original-broker"

    @property
    def exchange_backup(self) -> Path:
        return self.state / "original-exchange"

    @property
    def created_enable_parent_marker(self) -> Path:
        return self.state / "created-enable-directory"


def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _safe_parents(path: Path) -> None:
    for parent in reversed(path.parents):
        info = parent.lstat()
        if (not stat.S_ISDIR(info.st_mode) or info.st_uid != 0
                or stat.S_IMODE(info.st_mode) & 0o022):
            raise RuntimeError("deployment parent is not root-owned and fixed")


def _read_fixed(path: Path, expected_sha256: str, mode: int,
                *, enforce_owner: bool) -> bytes:
    info = path.lstat()
    if (not stat.S_ISREG(info.st_mode) or info.st_nlink != 1
            or (enforce_owner and (
                stat.S_IMODE(info.st_mode) != mode or info.st_uid != 0
            ))):
        raise RuntimeError("deployment file metadata mismatch")
    if enforce_owner:
        _safe_parents(path)
    value = path.read_bytes()
    if digest(value) != expected_sha256:
        raise RuntimeError("deployment file digest mismatch")
    return value


def _fsync_directory(path: Path, *, enforce_owner: bool) -> None:
    if not enforce_owner:  # Windows local fixture tests have no O_DIRECTORY.
        return
    descriptor = os.open(path, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _atomic_write(path: Path, value: bytes, mode: int,
                  *, enforce_owner: bool) -> None:
    descriptor, temporary = tempfile.mkstemp(prefix=".qaos-pilot-", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(value)
            stream.flush()
            os.fchmod(stream.fileno(), mode)
            if enforce_owner:
                os.fchown(stream.fileno(), 0, 0)
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        _fsync_directory(path.parent, enforce_owner=enforce_owner)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def _unlink_exact(path: Path, expected_sha256: str, mode: int,
                  *, enforce_owner: bool) -> None:
    if not path.exists() and not path.is_symlink():
        return
    _read_fixed(path, expected_sha256, mode, enforce_owner=enforce_owner)
    if not enforce_owner:  # Windows fixture marks mode 0400 as undeletable.
        path.chmod(0o600)
    path.unlink()
    _fsync_directory(path.parent, enforce_owner=enforce_owner)


def _prepare(layout: Layout, *, enforce_owner: bool) -> tuple[bytes, bytes]:
    if layout.state.exists() or layout.state.is_symlink():
        raise RuntimeError("pilot upgrade state already exists")
    if layout.enable.exists() or layout.enable.is_symlink():
        raise RuntimeError("pilot enable control already exists")
    if layout.pilot_launcher.exists() or layout.pilot_launcher.is_symlink():
        raise RuntimeError("pilot launcher already exists")
    if enforce_owner:
        info = layout.stage.lstat()
        if (not stat.S_ISDIR(info.st_mode) or info.st_uid != 0
                or stat.S_IMODE(info.st_mode) != 0o700):
            raise RuntimeError("pilot stage is not root-owned and private")
        _safe_parents(layout.stage)
        deploy_info = layout.staged_deploy.lstat()
        if (not stat.S_ISREG(deploy_info.st_mode) or deploy_info.st_uid != 0
                or deploy_info.st_nlink != 1
                or stat.S_IMODE(deploy_info.st_mode) != 0o500):
            raise RuntimeError("staged deployment program metadata mismatch")
        # Its reviewed source digest must be checked independently at the live gate.
    original = _read_fixed(
        layout.broker, OLD_BROKER_SHA256, 0o755, enforce_owner=enforce_owner
    )
    original_exchange = _read_fixed(layout.exchange, OLD_EXCHANGE_SHA256, 0o644,
                                    enforce_owner=enforce_owner)
    _read_fixed(layout.staged_exchange, NEW_EXCHANGE_SHA256, 0o400,
                enforce_owner=enforce_owner)
    _read_fixed(layout.staged_broker, NEW_BROKER_SHA256, 0o400,
                enforce_owner=enforce_owner)
    _read_fixed(layout.staged_launcher, PILOT_LAUNCHER_SHA256, 0o400,
                enforce_owner=enforce_owner)
    return original, original_exchange


def arm_rollback(layout: Layout) -> None:
    subprocess.run(
        ["/usr/bin/systemd-run", "--unit=" + TIMER_UNIT, "--on-active=15m",
         "/usr/bin/python3", str(layout.staged_deploy), "rollback"],
        check=True, timeout=30, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    subprocess.run(
        ["/usr/bin/systemctl", "is-active", "--quiet", TIMER_UNIT + ".timer"],
        check=True, timeout=15, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )


@contextmanager
def deployment_lock():
    """Serialize the installer and its scheduled rollback on the Linux host."""
    import fcntl  # Linux-only; the CLI refuses other platforms.

    descriptor = os.open(
        LOCK_PATH, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600
    )
    try:
        info = os.fstat(descriptor)
        if (not stat.S_ISREG(info.st_mode) or info.st_uid != 0
                or info.st_nlink != 1 or stat.S_IMODE(info.st_mode) != 0o600):
            raise RuntimeError("deployment lock metadata mismatch")
        fcntl.flock(descriptor, fcntl.LOCK_EX)
        yield
    finally:
        os.close(descriptor)


def install(layout: Layout, arm: Callable[[Layout], None] = arm_rollback,
            *, enforce_owner: bool = True) -> None:
    original, original_exchange = _prepare(layout, enforce_owner=enforce_owner)
    layout.state.mkdir(mode=0o700)
    if enforce_owner:
        os.chown(layout.state, 0, 0)
        _safe_parents(layout.broker_backup)
    _atomic_write(layout.broker_backup, original, 0o400,
                  enforce_owner=enforce_owner)
    _atomic_write(layout.exchange_backup, original_exchange, 0o400,
                  enforce_owner=enforce_owner)
    # The backup exists before the timer; the timer is active before live paths change.
    arm(layout)
    try:
        if not layout.enable.parent.exists():
            layout.enable.parent.mkdir(mode=0o755)
            if enforce_owner:
                os.chown(layout.enable.parent, 0, 0)
                _fsync_directory(layout.enable.parent.parent, enforce_owner=True)
            try:
                _atomic_write(
                    layout.created_enable_parent_marker, CREATED_DIRECTORY_BYTES,
                    0o400, enforce_owner=enforce_owner,
                )
            except Exception:
                layout.enable.parent.rmdir()
                raise
        elif enforce_owner:
            _safe_parents(layout.enable)
            info = layout.enable.parent.lstat()
            if (not stat.S_ISDIR(info.st_mode) or info.st_uid != 0
                    or stat.S_IMODE(info.st_mode) & 0o022):
                raise RuntimeError("pilot enable directory is unsafe")
        launcher = _read_fixed(layout.staged_launcher, PILOT_LAUNCHER_SHA256,
                               0o400, enforce_owner=enforce_owner)
        _atomic_write(layout.pilot_launcher, launcher, 0o755,
                      enforce_owner=enforce_owner)
        exchange = _read_fixed(layout.staged_exchange, NEW_EXCHANGE_SHA256,
                               0o400, enforce_owner=enforce_owner)
        _read_fixed(layout.exchange, OLD_EXCHANGE_SHA256, 0o644,
                    enforce_owner=enforce_owner)
        _atomic_write(layout.exchange, exchange, 0o644,
                      enforce_owner=enforce_owner)
        broker = _read_fixed(layout.staged_broker, NEW_BROKER_SHA256,
                             0o400, enforce_owner=enforce_owner)
        _read_fixed(layout.broker, OLD_BROKER_SHA256, 0o755,
                    enforce_owner=enforce_owner)
        _atomic_write(layout.broker, broker, 0o755,
                      enforce_owner=enforce_owner)
        _atomic_write(layout.enable, ENABLE_BYTES, 0o400,
                      enforce_owner=enforce_owner)
        _read_fixed(layout.pilot_launcher, PILOT_LAUNCHER_SHA256, 0o755,
                    enforce_owner=enforce_owner)
        _read_fixed(layout.exchange, NEW_EXCHANGE_SHA256, 0o644,
                    enforce_owner=enforce_owner)
        _read_fixed(layout.broker, NEW_BROKER_SHA256, 0o755,
                    enforce_owner=enforce_owner)
        _read_fixed(layout.enable, digest(ENABLE_BYTES), 0o400,
                    enforce_owner=enforce_owner)
    except Exception:
        rollback(layout, enforce_owner=enforce_owner)
        raise


def rollback(layout: Layout, *, enforce_owner: bool = True) -> None:
    # Remove admission first, even when a backup is missing or corrupt.
    _unlink_exact(layout.enable, digest(ENABLE_BYTES), 0o400,
                  enforce_owner=enforce_owner)
    original = _read_fixed(layout.broker_backup, OLD_BROKER_SHA256, 0o400,
                           enforce_owner=enforce_owner)
    original_exchange = _read_fixed(layout.exchange_backup, OLD_EXCHANGE_SHA256,
                                    0o400, enforce_owner=enforce_owner)
    current = digest(layout.broker.read_bytes())
    if current == NEW_BROKER_SHA256:
        _read_fixed(layout.broker, NEW_BROKER_SHA256, 0o755,
                    enforce_owner=enforce_owner)
        _atomic_write(layout.broker, original, 0o755,
                      enforce_owner=enforce_owner)
    elif current != OLD_BROKER_SHA256:
        raise RuntimeError("broker changed outside pilot deployment")
    _read_fixed(layout.broker, OLD_BROKER_SHA256, 0o755,
                enforce_owner=enforce_owner)
    current_exchange = digest(layout.exchange.read_bytes())
    if current_exchange == NEW_EXCHANGE_SHA256:
        _read_fixed(layout.exchange, NEW_EXCHANGE_SHA256, 0o644,
                    enforce_owner=enforce_owner)
        _atomic_write(layout.exchange, original_exchange, 0o644,
                      enforce_owner=enforce_owner)
    elif current_exchange != OLD_EXCHANGE_SHA256:
        raise RuntimeError("protocol changed outside pilot deployment")
    _read_fixed(layout.exchange, OLD_EXCHANGE_SHA256, 0o644,
                enforce_owner=enforce_owner)
    _unlink_exact(layout.pilot_launcher, PILOT_LAUNCHER_SHA256, 0o755,
                  enforce_owner=enforce_owner)
    if layout.created_enable_parent_marker.exists():
        _read_fixed(
            layout.created_enable_parent_marker, digest(CREATED_DIRECTORY_BYTES),
            0o400, enforce_owner=enforce_owner,
        )
        layout.enable.parent.rmdir()  # Never remove a pre-existing or nonempty dir.
        _fsync_directory(layout.enable.parent.parent, enforce_owner=enforce_owner)
        _unlink_exact(
            layout.created_enable_parent_marker, digest(CREATED_DIRECTORY_BYTES),
            0o400, enforce_owner=enforce_owner,
        )


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    layout = Layout.production()
    if (sys.platform != "linux" or os.geteuid() != 0
            or Path(__file__).resolve() != layout.staged_deploy):
        return 2
    with deployment_lock():
        if args == ["install"]:
            install(layout)
            print("pilot-installed-with-targeted-rollback-armed")
            return 0
        if args == ["rollback"]:
            rollback(layout)
            print("pilot-targeted-rollback-complete")
            return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
