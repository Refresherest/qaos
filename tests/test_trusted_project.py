import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

from qaos.application import OperationalSession
from qaos.capabilities.python_project import PythonProjectCapability
from qaos.capabilities import python_project as project_module
from qaos.capabilities.text_stats_project import MEMBERS
from qaos.planner import PythonProjectIntent, Task
from qaos.planner.intents import intent_from_dict
from qaos.storage import create_stores

pytestmark = pytest.mark.skipif(sys.platform != "win32", reason="Windows publication contract")


def snapshot(path):
    return {str(p.relative_to(path)): (p.read_bytes(), p.stat().st_mtime_ns)
            for p in path.rglob("*") if p.is_file()}


def setup(root, enabled=("text_stats_project_v1",)):
    output = root / "output"
    output.mkdir(parents=True)
    stores = create_stores(root / "state")
    return output, stores, OperationalSession(stores, python_project_workspace=output,
                                             enabled_python_projects=enabled)


def build(session):
    obj = session.create_objective("plan trusted project")
    return obj, session.execute_intent(obj, PythonProjectIntent("Example"))


def assert_failed(stores):
    assert stores.objective_db.load()[0]["status"] == "failed"
    assert stores.plan_db.load()[0]["tasks"][0]["status"] == "failed"
    item = next(r for r in stores.queue_db.load() if r.get("task_id"))
    assert item["status"] == item["action"]["status"] == "failed"
    return item


def test_public_success_standalone_and_serialization(tmp_path):
    output, stores, session = setup(tmp_path)
    obj, result = build(session)
    assert result.completed and obj.status == "completed"
    assert {p.name for p in output.iterdir()} == {"Example"}
    project = output / "Example"
    assert {p.name: p.read_text(encoding="utf-8") for p in project.iterdir()} == dict(MEMBERS)
    task = Task.from_dict(stores.plan_db.load()[0]["tasks"][0])
    assert task.intent == PythonProjectIntent("Example")
    item = next(r for r in stores.queue_db.load() if r.get("task_id"))
    assert item["result"]["published"] is True and item["result"]["cli_cases_passed"] == 15
    assert set(item["result"]["member_sha256"]) == set(MEMBERS)
    before = snapshot(output)
    run = subprocess.run([sys.executable, "-E", "-s", "-B", str(project / "app.py"),
                          "--text", "hello world"], cwd=project,
                         capture_output=True, text=True, timeout=5, shell=False)
    assert run.returncode == 0 and run.stderr == ""
    assert json.loads(run.stdout) == {"characters": 11, "words": 2, "lines": 1}
    assert snapshot(output) == before


@pytest.mark.parametrize("name", ["../x", "CON", "com1", "a/b", "a.b", "", "a" * 65, "猫", "C:x"])
def test_invalid_names(name):
    with pytest.raises(ValueError):
        PythonProjectIntent(name)


@pytest.mark.parametrize("field,value", [("version", True), ("version", 2), ("source", "x"),
                                        ("template_id", "unknown")])
def test_bad_serialized_intent(field, value):
    record = PythonProjectIntent("Example").to_dict()
    record[field] = value
    with pytest.raises(ValueError):
        intent_from_dict(record)


def test_disabled_and_missing_workspace(tmp_path):
    output, stores, session = setup(tmp_path, ())
    obj = session.create_objective("plan disabled")
    before = snapshot(tmp_path)
    with pytest.raises(RuntimeError, match="not enabled"):
        session.execute_intent(obj, PythonProjectIntent("Example"))
    assert snapshot(tmp_path) == before
    with pytest.raises(ValueError, match="workspace"):
        OperationalSession(stores, enabled_python_projects=("text_stats_project_v1",))
    old = OperationalSession(stores, python_file_workspace=output,
                             enabled_python_templates=("text_stats_v1", "text_stats_cli_v1"))
    obj = old.create_objective("plan no project permission")
    before = snapshot(tmp_path)
    with pytest.raises(ValueError, match="not enabled"):
        old.execute_intent(obj, PythonProjectIntent("Example"))
    assert snapshot(tmp_path) == before


@pytest.mark.parametrize("kind", ["empty", "file", "nonempty"])
def test_existing_destination_preserved(tmp_path, kind):
    output, stores, session = setup(tmp_path)
    dst = output / "Example"
    if kind == "file":
        dst.write_text("existing")
    else:
        dst.mkdir()
        if kind == "nonempty":
            (dst / "existing").write_text("keep")
    before = snapshot(output)
    with pytest.raises(FileExistsError):
        build(session)
    assert snapshot(output) == before
    assert_failed(stores)


@pytest.mark.parametrize("fault", ["missing", "corrupt", "extra"])
def test_member_faults_and_cleanup(tmp_path, monkeypatch, fault):
    output, stores, session = setup(tmp_path)
    original = PythonProjectCapability._populate
    def faulty(self, stage):
        original(self, stage)
        if fault == "missing":
            (stage / "stats.py").unlink()
        elif fault == "corrupt":
            (stage / "stats.py").write_text("broken")
        else:
            (stage / "unexpected").write_text("do not delete unknown content")
    monkeypatch.setattr(PythonProjectCapability, "_populate", faulty)
    with pytest.raises(RuntimeError):
        build(session)
    assert not (output / "Example").exists()
    item = assert_failed(stores)
    if fault == "extra":
        assert item["result"]["cleanup_error"] == "RuntimeError"
        assert (output / item["result"]["residual_stage"] / "unexpected").exists()
    else:
        assert not list(output.iterdir())


def test_cleanup_error_is_reported(tmp_path, monkeypatch):
    output, stores, session = setup(tmp_path)
    def fail(*args):
        raise PermissionError("injected")
    monkeypatch.setattr(PythonProjectCapability, "_verify", fail)
    monkeypatch.setattr(PythonProjectCapability, "_cleanup", fail)
    with pytest.raises(RuntimeError, match="cleanup failed"):
        build(session)
    item = assert_failed(stores)
    assert item["result"]["cleanup_error"] == "PermissionError"
    assert (output / item["result"]["residual_stage"]).is_dir()


def test_post_publish_fault_and_recovery_refusal(tmp_path, monkeypatch):
    output, stores, session = setup(tmp_path)
    original = PythonProjectCapability._check_members
    def fail_final(self, directory):
        if directory.name == "Example":
            raise RuntimeError("injected post-publication fault")
        return original(self, directory)
    monkeypatch.setattr(PythonProjectCapability, "_check_members", fail_final)
    with pytest.raises(RuntimeError, match="post-publication"):
        build(session)
    item = assert_failed(stores)
    assert item["result"]["published"] is True
    before = snapshot(output)
    identity = stores.objective_db.load()[0]["objective_id"]
    for options in ({}, {"python_file_workspace": output}, {"python_project_workspace": output}):
        before_all = snapshot(tmp_path)
        with pytest.raises(ValueError, match="not enabled"):
            OperationalSession(stores, **options).recover_objective(identity)
        assert snapshot(tmp_path) == before_all
    with pytest.raises(FileExistsError):
        session.recover_objective(identity)
    assert snapshot(output) == before


def test_pre_publish_failure_explicit_recovery(tmp_path, monkeypatch):
    output, stores, session = setup(tmp_path)
    original = PythonProjectCapability._verify
    def fail(*args):
        raise RuntimeError("injected acceptance failure")
    monkeypatch.setattr(PythonProjectCapability, "_verify", fail)
    with pytest.raises(RuntimeError):
        build(session)
    assert not list(output.iterdir())
    assert_failed(stores)
    monkeypatch.setattr(PythonProjectCapability, "_verify", original)
    identity = stores.objective_db.load()[0]["objective_id"]
    reloaded = OperationalSession(stores, python_project_workspace=output,
                                  enabled_python_projects=("text_stats_project_v1",))
    assert reloaded.recover_objective(identity).status == "completed"
    assert (output / "Example" / "app.py").exists()


def test_publication_race_preserves_other_output(tmp_path, monkeypatch):
    output, stores, session = setup(tmp_path)
    original = PythonProjectCapability._publish
    def raced(self, stage, target):
        target.mkdir()
        (target / "owner.txt").write_text("other publisher")
        return original(self, stage, target)
    monkeypatch.setattr(PythonProjectCapability, "_publish", raced)
    with pytest.raises(FileExistsError):
        build(session)
    assert {p.name for p in output.iterdir()} == {"Example"}
    assert (output / "Example" / "owner.txt").read_text() == "other publisher"
    assert_failed(stores)


def test_corrupted_cli_fails_independent_acceptance(tmp_path, monkeypatch):
    broken = dict(MEMBERS)
    broken["app.py"] = broken["app.py"].replace("json.dumps(text_stats(text), sort_keys=True)",
                                               "json.dumps({}, sort_keys=True)")
    assert broken["app.py"] != MEMBERS["app.py"]
    monkeypatch.setattr(project_module, "MEMBERS", broken)
    output, stores, session = setup(tmp_path)
    with pytest.raises(RuntimeError, match="CLI acceptance"):
        build(session)
    assert not list(output.iterdir())
    assert assert_failed(stores)["result"]["cli_cases_passed"] == 0


def test_simulated_reparse_root_rejected(tmp_path, monkeypatch):
    from types import SimpleNamespace
    original = Path.lstat
    def flagged(path):
        result = original(path)
        if path == tmp_path:
            return SimpleNamespace(st_mode=result.st_mode, st_file_attributes=0x400)
        return result
    monkeypatch.setattr(Path, "lstat", flagged)
    with pytest.raises(ValueError, match="reparse"):
        PythonProjectCapability(tmp_path)


def test_unsupported_platform_fails_closed(tmp_path, monkeypatch):
    monkeypatch.setattr(project_module.sys, "platform", "unsupported")
    with pytest.raises(RuntimeError, match="Windows NTFS"):
        PythonProjectCapability(tmp_path)


def test_staging_ownership_change_refuses_cleanup(tmp_path):
    output, _, _ = setup(tmp_path)
    cap = PythonProjectCapability(output)
    stage = output / ".qaos-stage-test"
    stage.mkdir()
    (stage / "stats.py").write_text("preserve")
    with pytest.raises(RuntimeError, match="ownership"):
        cap._cleanup(stage, stage.stat().st_ino + 1)
    assert (stage / "stats.py").read_text() == "preserve"


def test_two_workspaces_isolated(tmp_path):
    _, _, first = setup(tmp_path / "first")
    setup(tmp_path / "second")
    before = snapshot(tmp_path / "second")
    build(first)
    assert snapshot(tmp_path / "second") == before


def test_fresh_process_public_build_and_discovery(tmp_path):
    output = tmp_path / "output"
    output.mkdir()
    state = tmp_path / "state"
    code = """import sys
from pathlib import Path
from qaos.application import OperationalSession
from qaos.storage import create_stores
from qaos.planner import PythonProjectIntent
s = OperationalSession(create_stores(Path(sys.argv[1])),
    python_project_workspace=Path(sys.argv[2]), enabled_python_projects=('text_stats_project_v1',))
assert s.execute_intent(s.create_objective('plan fresh project'), PythonProjectIntent('Example')).completed
"""
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1] / "src")
    run = subprocess.run([sys.executable, "-c", code, str(state), str(output)],
                         env=env, capture_output=True, text=True, timeout=110, shell=False)
    assert run.returncode == 0, run.stderr
    before = snapshot(tmp_path)
    listing = subprocess.run([sys.executable, "-m", "qaos.main", "objectives", "--workspace", str(state)],
                             env=env, capture_output=True, text=True, timeout=10, shell=False)
    assert listing.returncode == 0
    assert json.loads(listing.stdout.splitlines()[1])["status"] == "completed"
    assert snapshot(tmp_path) == before


def test_interruption_after_rename_preserves_project(tmp_path, monkeypatch):
    output, stores, session = setup(tmp_path)
    original = PythonProjectCapability._publish
    def interrupted(self, stage, target):
        original(self, stage, target)
        raise RuntimeError("interrupted after rename")
    monkeypatch.setattr(PythonProjectCapability, "_publish", interrupted)
    with pytest.raises(RuntimeError, match="interrupted"):
        build(session)
    item = assert_failed(stores)
    assert item["result"]["publication_uncertain"] is True
    assert item["result"]["published"] is None
    assert {p.name for p in (output / "Example").iterdir()} == set(MEMBERS)
