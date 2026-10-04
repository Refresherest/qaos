"""Local fixture tests for the targeted pilot deployment bridge (WO-176)."""

import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

TOOLS = Path(__file__).parents[1] / "tools" / "qaos-worker"
sys.path.insert(0, str(TOOLS))

import qaos_worker_pilot_deploy as deploy


@pytest.fixture
def layout(tmp_path, monkeypatch):
    old_broker = b"last verified synthetic broker"
    new_broker = b"fixed opt-in pilot broker"
    exchange = b"last verified synthetic protocol"
    new_exchange = b"fixed dual-runtime protocol"
    pilot_launcher = b"fixed pilot launcher"
    monkeypatch.setattr(deploy, "OLD_BROKER_SHA256", deploy.digest(old_broker))
    monkeypatch.setattr(deploy, "NEW_BROKER_SHA256", deploy.digest(new_broker))
    monkeypatch.setattr(deploy, "OLD_EXCHANGE_SHA256", deploy.digest(exchange))
    monkeypatch.setattr(deploy, "NEW_EXCHANGE_SHA256", deploy.digest(new_exchange))
    monkeypatch.setattr(deploy, "PILOT_LAUNCHER_SHA256", deploy.digest(pilot_launcher))

    fixture = deploy.Layout(
        stage=tmp_path / "stage",
        state=tmp_path / "state",
        broker=tmp_path / "sbin" / "qaos-worker-broker",
        exchange=tmp_path / "sbin" / "qaos_worker_exchange.py",
        pilot_launcher=tmp_path / "sbin" / "qaos-worker-pilot-launcher",
        enable=tmp_path / "etc" / "qaos-worker" / "enable-python-single-v1",
    )
    fixture.stage.mkdir()
    fixture.broker.parent.mkdir()
    fixture.enable.parent.parent.mkdir()
    fixture.broker.write_bytes(old_broker)
    fixture.exchange.write_bytes(exchange)
    fixture.staged_exchange.write_bytes(new_exchange)
    fixture.staged_broker.write_bytes(new_broker)
    fixture.staged_launcher.write_bytes(pilot_launcher)
    fixture.staged_deploy.write_bytes(b"local fixture only")
    return fixture


def test_installer_arms_rollback_before_live_path_change_and_preserves_transport(
    layout, tmp_path
):
    synthetic_launcher = tmp_path / "sbin" / "qaos-worker-launcher"
    synthetic_launcher.write_bytes(b"existing synthetic launcher")
    authorized_keys = tmp_path / "authorized_keys"
    authorized_keys.write_bytes(b"existing restricted identity")
    sudoers = tmp_path / "sudoers"
    sudoers.write_bytes(b"existing broker grant")
    observed = []

    def arm(fixture):
        observed.append("armed")
        assert fixture.broker.read_bytes() == b"last verified synthetic broker"
        assert fixture.broker_backup.read_bytes() == fixture.broker.read_bytes()
        assert fixture.exchange_backup.read_bytes() == fixture.exchange.read_bytes()
        assert not fixture.pilot_launcher.exists()
        assert not fixture.enable.exists()

    deploy.install(layout, arm, enforce_owner=False)
    assert observed == ["armed"]
    assert layout.broker.read_bytes() == b"fixed opt-in pilot broker"
    assert layout.pilot_launcher.read_bytes() == b"fixed pilot launcher"
    assert layout.enable.read_bytes() == deploy.ENABLE_BYTES
    assert layout.created_enable_parent_marker.read_bytes() == deploy.CREATED_DIRECTORY_BYTES
    assert synthetic_launcher.read_bytes() == b"existing synthetic launcher"
    assert layout.exchange.read_bytes() == b"fixed dual-runtime protocol"
    assert authorized_keys.read_bytes() == b"existing restricted identity"
    assert sudoers.read_bytes() == b"existing broker grant"

    deploy.rollback(layout, enforce_owner=False)
    assert layout.broker.read_bytes() == b"last verified synthetic broker"
    assert layout.exchange.read_bytes() == b"last verified synthetic protocol"
    assert not layout.pilot_launcher.exists()
    assert not layout.enable.exists()
    assert not layout.enable.parent.exists()
    assert layout.broker_backup.read_bytes() == b"last verified synthetic broker"
    deploy.rollback(layout, enforce_owner=False)  # Timer and manual rollback can race.
    assert synthetic_launcher.read_bytes() == b"existing synthetic launcher"
    assert authorized_keys.read_bytes() == b"existing restricted identity"
    assert sudoers.read_bytes() == b"existing broker grant"


@pytest.mark.parametrize("target", [
    "broker", "exchange", "staged_broker", "staged_exchange", "staged_launcher",
])
def test_installer_refuses_digest_drift_before_arming(layout, target):
    getattr(layout, target).write_bytes(b"unexpected bytes")
    observed = []
    with pytest.raises(RuntimeError, match="digest mismatch"):
        deploy.install(layout, observed.append, enforce_owner=False)
    assert observed == []
    assert not layout.state.exists()
    assert not layout.enable.exists()


def test_installer_refuses_existing_pilot_state(layout):
    layout.enable.parent.mkdir(parents=True)
    layout.enable.write_bytes(deploy.ENABLE_BYTES)
    with pytest.raises(RuntimeError, match="control already exists"):
        deploy.install(layout, lambda unused: pytest.fail("must not arm"),
                       enforce_owner=False)
    assert layout.broker.read_bytes() == b"last verified synthetic broker"


def test_rollback_preserves_preexisting_enable_directory(layout):
    layout.enable.parent.mkdir()
    deploy.install(layout, lambda unused: None, enforce_owner=False)
    assert not layout.created_enable_parent_marker.exists()
    deploy.rollback(layout, enforce_owner=False)
    assert layout.enable.parent.is_dir()


def test_timer_failure_cannot_change_live_paths(layout):
    def fail_timer(unused):
        raise RuntimeError("timer unavailable")

    with pytest.raises(RuntimeError, match="timer unavailable"):
        deploy.install(layout, fail_timer, enforce_owner=False)
    assert layout.broker.read_bytes() == b"last verified synthetic broker"
    assert not layout.pilot_launcher.exists()
    assert not layout.enable.exists()
    assert layout.broker_backup.read_bytes() == layout.broker.read_bytes()
    assert layout.exchange_backup.read_bytes() == layout.exchange.read_bytes()


def test_post_arm_install_failure_uses_targeted_rollback(layout, monkeypatch):
    original_write = deploy._atomic_write
    injected = False

    def fail_once(path, value, mode, *, enforce_owner):
        nonlocal injected
        if path == layout.enable and not injected:
            injected = True
            raise RuntimeError("injected enable failure")
        return original_write(path, value, mode, enforce_owner=enforce_owner)

    monkeypatch.setattr(deploy, "_atomic_write", fail_once)
    with pytest.raises(RuntimeError, match="injected enable failure"):
        deploy.install(layout, lambda unused: None, enforce_owner=False)
    assert layout.broker.read_bytes() == b"last verified synthetic broker"
    assert layout.exchange.read_bytes() == b"last verified synthetic protocol"
    assert not layout.pilot_launcher.exists()
    assert not layout.enable.exists()


def test_rollback_refuses_unrecognized_broker_after_disabling_pilot(layout):
    deploy.install(layout, lambda unused: None, enforce_owner=False)
    layout.broker.write_bytes(b"unrelated root change")
    with pytest.raises(RuntimeError, match="changed outside pilot"):
        deploy.rollback(layout, enforce_owner=False)
    assert not layout.enable.exists()
    assert layout.broker.read_bytes() == b"unrelated root change"
    assert layout.exchange.read_bytes() == b"fixed dual-runtime protocol"
    assert layout.pilot_launcher.read_bytes() == b"fixed pilot launcher"


def test_rollback_disables_pilot_even_when_backup_is_corrupt(layout):
    deploy.install(layout, lambda unused: None, enforce_owner=False)
    layout.broker_backup.chmod(0o600)  # Windows fixture mode 0400 is read-only.
    layout.broker_backup.write_bytes(b"corrupted backup")
    with pytest.raises(RuntimeError, match="digest mismatch"):
        deploy.rollback(layout, enforce_owner=False)
    assert not layout.enable.exists()
    assert layout.broker.read_bytes() == b"fixed opt-in pilot broker"
    assert layout.exchange.read_bytes() == b"fixed dual-runtime protocol"


def test_timer_invokes_only_fixed_targeted_rollback(layout, monkeypatch):
    calls = []

    def fake_run(argv, **kwargs):
        calls.append((argv, kwargs))
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(deploy.subprocess, "run", fake_run)
    deploy.arm_rollback(layout)
    assert calls[0][0] == [
        "/usr/bin/systemd-run", "--unit=qaos-worker-pilot-rollback",
        "--on-active=15m", "/usr/bin/python3", str(layout.staged_deploy),
        "rollback",
    ]
    assert calls[1][0] == [
        "/usr/bin/systemctl", "is-active", "--quiet",
        "qaos-worker-pilot-rollback.timer",
    ]
    assert all(call[1]["check"] is True for call in calls)


def test_production_layout_and_cli_do_not_accept_caller_paths():
    fixed = deploy.Layout.production()
    assert fixed.broker == Path("/usr/local/sbin/qaos-worker-broker")
    assert fixed.pilot_launcher == Path("/usr/local/sbin/qaos-worker-pilot-launcher")
    assert fixed.enable == Path("/etc/qaos-worker/enable-python-single-v1")
    assert deploy.digest((TOOLS / "qaos_worker_broker.py").read_bytes()) == deploy.NEW_BROKER_SHA256
    assert deploy.digest((TOOLS / "qaos_worker_exchange.py").read_bytes()) == deploy.NEW_EXCHANGE_SHA256
    assert deploy.digest((TOOLS / "qaos_worker_pilot_launcher.py").read_bytes()) == deploy.PILOT_LAUNCHER_SHA256
    assert deploy.main(["--root", "other", "install"]) == 2
