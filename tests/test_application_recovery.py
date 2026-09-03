"""Application recovery contract under OWNER-DECISION-017."""

import pytest

from qaos.application import OperationalSession
from qaos.executive.manager import ExecutiveManager
from qaos.objectives import Objective
from qaos.storage import create_stores


def build_failed_attempt(path):
    stores = create_stores(path)
    stores.objective_db.save([{
        "goal": "recover work", "objective_id": "objective-1", "status": "failed"
    }])
    tasks = [
        {"description": "planning", "task_id": f"task-{index}", "status": status}
        for index, status in enumerate(("completed", "failed", "pending"))
    ]
    stores.plan_db.save([{
        "objective": "recover work", "objective_id": "objective-1", "tasks": tasks
    }])
    stores.queue_db.save([
        {"objective": "recover work", "objective_id": "objective-1",
         "assignee": "default", "action": task, "task_id": task["task_id"],
         "status": task["status"]}
        for task in tasks
    ])
    return stores


def forbidden(*args, **kwargs):
    raise AssertionError("normal pipeline must not run during recovery")


def test_session_recovers_reloaded_attempt_without_pipeline(tmp_path, monkeypatch):
    stores = build_failed_attempt(tmp_path)
    session = OperationalSession(stores)
    executive = session._executive
    pipeline = executive._orchestrator._pipeline
    assert executive._recovery is pipeline._execution
    monkeypatch.setattr(executive._orchestrator, "execute", forbidden)
    monkeypatch.setattr(pipeline, "execute", forbidden)
    monkeypatch.setattr(session._kernel, "execute_objective", forbidden)
    for service, method in [
        (pipeline._classifier, "classify"), (pipeline._council, "delegate"),
        (pipeline._planner, "plan"), (pipeline._reflection, "reflect"),
        (pipeline._learning, "learn"),
    ]:
        monkeypatch.setattr(service, method, forbidden)

    result = session.recover_objective("objective-1")

    assert isinstance(result, Objective)
    assert result is session._objectives.get_by_id("objective-1")
    assert result.status == "completed"
    assert stores.objective_db.load()[0]["status"] == "completed"
    assert [item["status"] for item in stores.queue_db.load()] == ["completed"] * 3
    assert [task["status"] for task in stores.plan_db.load()[0]["tasks"]] == [
        "completed"
    ] * 3


@pytest.mark.parametrize("selector,error", [(None, TypeError), (42, TypeError),
                                           ("", ValueError), ("   ", ValueError)])
def test_invalid_selectors_never_delegate(tmp_path, monkeypatch, selector, error):
    session = OperationalSession(create_stores(tmp_path))
    monkeypatch.setattr(session._executive, "recover", forbidden)
    with pytest.raises(error):
        session.recover_objective(selector)


def test_no_goal_guessing_or_cross_workspace_lookup(tmp_path):
    first = build_failed_attempt(tmp_path / "first")
    second = create_stores(tmp_path / "second")
    session = OperationalSession(second)
    with pytest.raises(ValueError, match="not found"):
        session.recover_objective("objective-1")
    with pytest.raises(ValueError, match="not found"):
        OperationalSession(first).recover_objective("recover work")
    assert first.objective_db.load()[0]["status"] == "failed"
    assert second.objective_db.load() == []


def test_recovery_exception_propagates_without_wrapper(tmp_path, monkeypatch):
    stores = build_failed_attempt(tmp_path)
    session = OperationalSession(stores)
    original = RuntimeError("worker failure")
    from qaos.planner import Task

    def fail(task):
        raise original

    monkeypatch.setattr(Task, "complete", fail)
    with pytest.raises(RuntimeError) as raised:
        session.recover_objective("objective-1")
    assert raised.value is original
    assert stores.objective_db.load()[0]["status"] == "failed"


def test_missing_service_is_explicit():
    with pytest.raises(RuntimeError, match="No recovery service"):
        ExecutiveManager().recover("objective-1")
