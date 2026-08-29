"""Task identity and QueueItem action-reference tests."""

import pytest

from qaos.application import OperationalSession
from qaos.objectives import Objective
from qaos.planner import Plan, PlannerManager, Task
from qaos.queue import QueueItem, QueueManager
from qaos.storage import create_stores


def deterministic_ids(*values):
    generated = iter(values)
    return lambda: next(generated)


def test_planner_assigns_deterministic_immutable_task_identity(tmp_path):
    stores = create_stores(tmp_path)
    manager = PlannerManager(
        stores=stores,
        task_id_generator=deterministic_ids("task-1"),
    )
    plan = manager.create(Objective("identified task", objective_id="objective-1"))
    task = plan.add_task("work")

    manager.save()

    assert task.task_id == "task-1"
    assert plan.get_task_by_id("task-1") is task
    assert stores.plan_db.load()[0]["tasks"][0]["task_id"] == "task-1"

    with pytest.raises(ValueError, match="immutable"):
        task._assign_identity("task-2")


def test_legacy_task_remains_unidentified_on_unrelated_save(tmp_path):
    stores = create_stores(tmp_path)
    legacy = {
        "objective": "legacy plan",
        "tasks": [
            {
                "description": "legacy task",
                "status": "pending",
                "started": None,
                "completed": None,
            }
        ],
    }
    stores.plan_db.save([legacy])
    generator_calls = []
    manager = PlannerManager(
        stores=stores,
        task_id_generator=lambda: generator_calls.append(True) or "unexpected",
    )

    manager.save()

    assert manager.get("legacy plan").tasks[0].task_id is None
    assert generator_calls == []
    assert stores.plan_db.load() == [legacy]


def test_duplicate_task_identity_fails_closed_before_persistence(tmp_path):
    stores = create_stores(tmp_path)
    manager = PlannerManager(stores=stores)
    plan = manager.create("duplicate tasks")
    plan.add_task(Task("first", task_id="duplicate-id"))
    plan.add_task(Task("second", task_id="duplicate-id"))

    with pytest.raises(ValueError, match="duplicate task_id"):
        manager.save()

    assert stores.plan_db.load()[0]["tasks"] == []


def test_duplicate_persisted_task_identity_fails_closed_on_load(tmp_path):
    stores = create_stores(tmp_path)
    stores.plan_db.save(
        [
            {
                "objective": "duplicate tasks",
                "tasks": [
                    {"description": "first", "task_id": "duplicate-id"},
                    {"description": "second", "task_id": "duplicate-id"},
                ],
            }
        ]
    )

    with pytest.raises(ValueError, match="duplicate task_id"):
        PlannerManager(stores=stores)


def test_queue_item_copies_and_reloads_task_reference(tmp_path):
    stores = create_stores(tmp_path)
    task = Task("queued task", task_id="task-1")
    manager = QueueManager(stores=stores)
    item = QueueItem(
        Objective("queued objective", objective_id="objective-1"),
        "default",
        task,
    )

    manager.add(item)
    reloaded = QueueManager(stores=stores).items()[0]

    assert item.task_id == "task-1"
    assert reloaded.task_id == "task-1"
    assert reloaded.action.task_id == "task-1"
    assert stores.queue_db.load()[0]["task_id"] == "task-1"


def test_queue_item_rejects_mismatched_action_reference(tmp_path):
    stores = create_stores(tmp_path)
    stores.queue_db.save(
        [
            {
                "objective": "mismatch",
                "assignee": "default",
                "task_id": "task-1",
                "action": {"description": "work", "task_id": "task-2"},
            }
        ]
    )

    with pytest.raises(ValueError, match="does not match"):
        QueueManager(stores=stores)


def test_council_queue_item_has_no_task_reference():
    item = QueueItem(
        Objective("delegation", objective_id="objective-1"),
        "council member",
    )

    assert item.action is None
    assert item.task_id is None


def test_operational_pipeline_assigns_task_references_before_queueing(tmp_path):
    stores = create_stores(tmp_path)

    OperationalSession(stores).execute_goal("task identity pipeline")

    plan_tasks = stores.plan_db.load()[0]["tasks"]
    task_ids = {task["task_id"] for task in plan_tasks}
    action_items = [item for item in stores.queue_db.load() if item["action"]]

    assert len(task_ids) == len(plan_tasks)
    assert {item["task_id"] for item in action_items} == task_ids
    assert {item["action"]["task_id"] for item in action_items} == task_ids
