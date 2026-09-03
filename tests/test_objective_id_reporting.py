"""Explicit session ownership and pre-execution CLI identity."""

import pytest

from qaos.application import OperationalSession
from qaos.main import main
from qaos.objectives import Objective
from qaos.planner import Task
from qaos.storage import create_stores


def test_create_execute_has_one_canonical_record(tmp_path):
    stores = create_stores(tmp_path)
    session = OperationalSession(stores)
    objective = session.create_objective(" plan work ")
    assert objective.goal == "plan work"
    assert len(stores.objective_db.load()) == 1
    assert session.execute_objective(objective).objective is objective
    assert len(stores.objective_db.load()) == 1


def test_foreign_and_copied_objectives_rejected(tmp_path, monkeypatch):
    first = OperationalSession(create_stores(tmp_path / "first"))
    second = OperationalSession(create_stores(tmp_path / "second"))
    objective = first.create_objective("same goal")
    monkeypatch.setattr(second._kernel, "execute_objective",
                        lambda value: pytest.fail("must reject before execution"))
    with pytest.raises(ValueError, match="belong"):
        second.execute_objective(objective)
    with pytest.raises(ValueError, match="belong"):
        first.execute_objective(Objective(objective.goal, objective.objective_id))
    with pytest.raises(TypeError):
        first.execute_objective("raw goal")


def test_original_internal_exception_is_preserved(tmp_path, monkeypatch):
    session = OperationalSession(create_stores(tmp_path))
    objective = session.create_objective("failure")
    original = RuntimeError("original")
    def fail(value):
        raise original
    monkeypatch.setattr(session._kernel, "execute_objective", fail)
    with pytest.raises(RuntimeError) as raised:
        session.execute_objective(objective)
    assert raised.value is original
    assert objective.status == "failed"


def test_invalid_generated_identity_not_persisted(tmp_path):
    stores = create_stores(tmp_path)
    session = OperationalSession(stores)
    session._objectives._id_generator = lambda: ""
    with pytest.raises(ValueError):
        session.create_objective("invalid generated ID")
    assert stores.objective_db.load() == []


def test_cli_failure_reports_recoverable_id_first(tmp_path, monkeypatch, capsys):
    original = Task.complete
    count = 0
    def fail_second(task):
        nonlocal count
        count += 1
        if count == 2:
            raise RuntimeError("sensitive payload")
        return original(task)
    with monkeypatch.context() as patcher:
        patcher.setattr(Task, "complete", fail_second)
        assert main(["objective", "--workspace", str(tmp_path), "plan work"]) == 1
    output = capsys.readouterr()
    assert output.out.startswith("Objective ID: ")
    identity = output.out.splitlines()[0].removeprefix("Objective ID: ")
    stores = create_stores(tmp_path)
    assert identity == stores.objective_db.load()[0]["objective_id"]
    assert "sensitive payload" not in output.err + output.out
    assert main(["recover", "--workspace", str(tmp_path), identity]) == 0
    assert stores.objective_db.load()[0]["status"] == "completed"
