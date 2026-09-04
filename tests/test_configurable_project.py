import dataclasses
import itertools
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest
from qaos.application import OperationalSession
from qaos.capabilities import python_project
from qaos.capabilities.text_stats_project import MEMBERS
from qaos.capabilities.text_stats_project_v2 import render
from qaos.planner import PythonProjectIntentV2, PythonProjectIntent, Task
from qaos.planner.intents import intent_from_dict
from qaos.storage import create_stores


def snapshot(path):
    return {str(p.relative_to(path)): (p.read_bytes(), p.stat().st_mtime_ns)
            for p in path.rglob("*") if p.is_file()}


def setup(root, enabled=("text_stats_project_v1",)):
    output = root / "output"
    output.mkdir(parents=True)
    stores = create_stores(root / "state")
    return output, stores, OperationalSession(stores, python_project_workspace=output,
                                             enabled_python_projects=enabled)


def assert_failed(stores):
    assert stores.objective_db.load()[0]["status"] == "failed"
    assert stores.plan_db.load()[0]["tasks"][0]["status"] == "failed"
    item = next(r for r in stores.queue_db.load() if r.get("task_id"))
    assert item["status"] == item["action"]["status"] == "failed"

pytestmark = pytest.mark.skipif(sys.platform != "win32", reason="local Windows project contract")
V2 = ("text_stats_project_v2",)
KEYS = ("characters", "words", "lines")
SELECTIONS = [c for size in range(1, 4) for c in itertools.combinations(KEYS, size)]


@pytest.mark.parametrize("metrics", SELECTIONS)
def test_all_configurations_public_build(tmp_path, metrics):
    output, stores, session = setup(tmp_path, V2)
    intent = PythonProjectIntentV2("Example", metrics)
    assert session.execute_intent(session.create_objective("plan selected metrics"), intent).completed
    project = output / "Example"
    assert {p.name: p.read_text(encoding="utf-8") for p in project.iterdir()} == dict(render(metrics))
    assert (project / "stats.py").read_text(encoding="utf-8") == MEMBERS["stats.py"]
    row = next(r for r in stores.queue_db.load() if r.get("task_id"))
    assert row["result"]["metrics"] == list(metrics)
    assert row["result"]["cli_cases_passed"] == 15
    assert row["result"]["template_version"] == 2
    assert Task.from_dict(stores.plan_db.load()[0]["tasks"][0]).intent == intent
    for text, counts in (("", (0, 0, 0)), ("hello world", (11, 2, 1)),
                         ("one\ntwo", (7, 2, 2)), ("猫 café", (6, 2, 1))):
        result = subprocess.run([sys.executable, "-E", "-s", "-B", str(project / "app.py"), "--text", text],
                                cwd=project, capture_output=True, text=True, timeout=5)
        assert result.returncode == 0 and result.stderr == ""
        expected = {key: value for key, value in zip(KEYS, counts) if key in metrics}
        assert json.loads(result.stdout) == expected


@pytest.mark.parametrize("metrics", [[], ["words", "words"], ["unknown"], "words", None, [True], [{}], {"words"}])
def test_invalid_selection_no_writes(tmp_path, metrics):
    setup(tmp_path, V2)
    before = snapshot(tmp_path)
    with pytest.raises((ValueError, TypeError)):
        PythonProjectIntentV2("Example", metrics)
    assert snapshot(tmp_path) == before


def test_normalized_immutable_and_serialized_contract():
    values = ["lines", "characters"]
    intent = PythonProjectIntentV2("Example", values)
    values.clear()
    assert intent.metrics == ("characters", "lines")
    assert intent.to_dict()["metrics"] == ["characters", "lines"]
    assert intent_from_dict(intent.to_dict()) == intent
    with pytest.raises(dataclasses.FrozenInstanceError):
        intent.metrics = ("words",)
    for change in ({"metrics": ("words",)}, {"source": "anything"}, {"version": True},
                   {"version": 1}, {"template_id": "text_stats_project_v1"}):
        data = intent.to_dict() | change
        with pytest.raises((ValueError, TypeError)):
            intent_from_dict(data)
    data = intent.to_dict()
    del data["metrics"]
    with pytest.raises(ValueError):
        intent_from_dict(data)


def test_determinism_and_v1_same_session(tmp_path):
    output, _, session = setup(tmp_path, (*V2, "text_stats_project_v1"))
    for name, metrics in (("First", ["lines", "words"]), ("Second", ["words", "lines"])):
        session.execute_intent(session.create_objective("plan deterministic"), PythonProjectIntentV2(name, metrics))
    assert {p.name: p.read_bytes() for p in (output / "First").iterdir()} == {
        p.name: p.read_bytes() for p in (output / "Second").iterdir()}
    session.execute_intent(session.create_objective("plan old project"), PythonProjectIntent("Old"))
    assert {p.name: p.read_text(encoding="utf-8") for p in (output / "Old").iterdir()} == dict(MEMBERS)
    for metrics in SELECTIONS:
        assert render(metrics) == render(tuple(reversed(metrics)))
    assert len({render(m)["app.py"] for m in SELECTIONS}) == 7
    assert len({render(m)["test_stats.py"] for m in SELECTIONS}) == 7


def test_v1_permission_does_not_enable_v2(tmp_path):
    _, _, session = setup(tmp_path)
    obj = session.create_objective("plan unauthorized v2")
    before = snapshot(tmp_path)
    with pytest.raises(ValueError, match="not enabled"):
        session.execute_intent(obj, PythonProjectIntentV2("Example", ["words"]))
    assert snapshot(tmp_path) == before


def test_corruption_rejected_independently_and_recovery_preserves_metrics(tmp_path, monkeypatch):
    output, stores, session = setup(tmp_path, V2)
    original = python_project.render
    def broken(metrics):
        members = dict(original(metrics))
        members["app.py"] = members["app.py"].replace("for key in SELECTED_METRICS",
            "for key in (() if text == 'hello world' else SELECTED_METRICS)")
        return members
    monkeypatch.setattr(python_project, "render", broken)
    with pytest.raises(RuntimeError, match="CLI acceptance"):
        session.execute_intent(session.create_objective("plan bad selected output"),
                               PythonProjectIntentV2("Example", ["words"]))
    assert_failed(stores)
    assert not list(output.iterdir())
    identity = stores.objective_db.load()[0]["objective_id"]
    before = snapshot(tmp_path)
    with pytest.raises(ValueError, match="not enabled"):
        OperationalSession(stores, python_project_workspace=output,
                           enabled_python_projects=("text_stats_project_v1",)).recover_objective(identity)
    assert snapshot(tmp_path) == before
    monkeypatch.setattr(python_project, "render", original)
    assert OperationalSession(stores, python_project_workspace=output,
                              enabled_python_projects=V2).recover_objective(identity).status == "completed"
    assert (output / "Example" / "app.py").read_text(encoding="utf-8") == render(["words"])["app.py"]
    before = snapshot(output)
    with pytest.raises(FileExistsError):
        session.execute_intent(session.create_objective("plan collision"), PythonProjectIntentV2("Example", ["lines"]))
    assert snapshot(output) == before


def test_fresh_process_build_use_discovery(tmp_path):
    output = tmp_path / "output"
    output.mkdir()
    state = tmp_path / "state"
    code = """import sys
from pathlib import Path
from qaos.application import OperationalSession
from qaos.storage import create_stores
from qaos.planner import PythonProjectIntentV2
s = OperationalSession(create_stores(Path(sys.argv[1])), python_project_workspace=Path(sys.argv[2]),
    enabled_python_projects=('text_stats_project_v2',))
assert s.execute_intent(s.create_objective('plan configured project'), PythonProjectIntentV2('Example', ['words'])).completed
"""
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1] / "src")
    result = subprocess.run([sys.executable, "-c", code, str(state), str(output)], env=env,
                            capture_output=True, text=True, timeout=110)
    assert result.returncode == 0, result.stderr
    before = snapshot(tmp_path)
    result = subprocess.run([sys.executable, "-E", "-s", "-B", str(output / "Example" / "app.py"),
                             "--text", "hello world"], capture_output=True, text=True, timeout=5)
    assert result.returncode == 0 and json.loads(result.stdout) == {"words": 2}
    listing = subprocess.run([sys.executable, "-m", "qaos.main", "objectives", "--workspace", str(state)],
                             env=env, capture_output=True, text=True, timeout=10)
    assert listing.returncode == 0 and json.loads(listing.stdout.splitlines()[1])["status"] == "completed"
    assert snapshot(tmp_path) == before


def test_v2_publication_gap_and_isolation(tmp_path, monkeypatch):
    output, stores, session = setup(tmp_path / "first", V2)
    setup(tmp_path / "second", V2)
    untouched = snapshot(tmp_path / "second")
    original = python_project.PythonProjectCapability._check_members
    def fault(self, directory):
        if directory.name == "Example":
            raise RuntimeError("post-publication fault")
        return original(self, directory)
    monkeypatch.setattr(python_project.PythonProjectCapability, "_check_members", fault)
    with pytest.raises(RuntimeError, match="post-publication"):
        session.execute_intent(session.create_objective("plan v2 gap"), PythonProjectIntentV2("Example", ["lines"]))
    assert_failed(stores)
    assert snapshot(tmp_path / "second") == untouched
    before = snapshot(output)
    identity = stores.objective_db.load()[0]["objective_id"]
    with pytest.raises(FileExistsError):
        OperationalSession(stores, python_project_workspace=output, enabled_python_projects=V2).recover_objective(identity)
    assert snapshot(output) == before


def test_invalid_mutated_intent_rejected_before_execution_writes(tmp_path):
    _, _, session = setup(tmp_path, V2)
    obj = session.create_objective("plan invalid mutation")
    intent = PythonProjectIntentV2("Example", ["words"])
    object.__setattr__(intent, "metrics", ("unknown",))  # emulate corrupted in-memory input
    before = snapshot(tmp_path)
    with pytest.raises(ValueError):
        session.execute_intent(obj, intent)
    assert snapshot(tmp_path) == before
