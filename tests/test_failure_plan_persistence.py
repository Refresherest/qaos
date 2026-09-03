"""Real failure-to-reload recovery and exception preservation (FINDING-038)."""

from unittest.mock import patch

import pytest

from qaos.application import OperationalSession
from qaos.execution.engine import ExecutionEngine
from qaos.objectives import Objective
from qaos.planner import Plan, Task
from qaos.storage import create_stores


def test_real_failure_reload_and_targeted_recovery(tmp_path):
    stores = create_stores(tmp_path)
    original_complete = Task.complete
    completed_calls = []
    original = RuntimeError("second task fails")

    def fail_second(task):
        completed_calls.append(task.task_id)
        if len(completed_calls) == 2:
            raise original
        return original_complete(task)

    with patch.object(Task, "complete", fail_second):
        with pytest.raises(RuntimeError) as raised:
            OperationalSession(stores).execute_goal("plan recovery integration")
    assert raised.value is original
    tasks = stores.plan_db.load()[0]["tasks"]
    actions = [item["action"] for item in stores.queue_db.load() if item["action"]]
    assert tasks == actions
    assert [task["status"] for task in tasks] == [
        "completed", "failed", "pending", "pending", "pending"
    ]
    completed_before = tasks[0].copy()
    queue_count = len(stores.queue_db.load())
    recovered_calls = []

    def record_complete(task):
        recovered_calls.append(task.task_id)
        return original_complete(task)

    with patch.object(Task, "complete", record_complete):
        result = OperationalSession(stores).recover_objective(
            stores.objective_db.load()[0]["objective_id"]
        )
    assert result.status == "completed"
    assert recovered_calls == [task["task_id"] for task in tasks[1:]]
    assert stores.plan_db.load()[0]["tasks"][0] == completed_before
    assert len(stores.queue_db.load()) == queue_count
    assert all(task["status"] == "completed"
               for task in stores.plan_db.load()[0]["tasks"])
    assert all(item["status"] == "completed" for item in stores.queue_db.load())
    assert stores.objective_db.load()[0]["status"] == "completed"


def test_cleanup_save_failure_preserves_execution_exception():
    original = RuntimeError("queue failure")
    calls = []

    class Planner:
        def get(self, objective):
            return Plan(objective)

        def save(self):
            calls.append("save")
            raise OSError("save failed")

    class Queue:
        def process(self):
            raise original

    with pytest.raises(RuntimeError) as raised:
        ExecutionEngine(planner=Planner(), queue=Queue()).execute(Objective("test"))
    assert raised.value is original
    assert calls == ["save"]
