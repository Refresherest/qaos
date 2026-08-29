"""Bounded explicit recovery tests for OWNER-DECISION-015."""

from datetime import datetime

import pytest

from qaos.execution import ExecutionEngine, ExecutionManager
from qaos.execution.registry import ExecutionRegistry
from qaos.objectives import ObjectiveManager
from qaos.planner import PlannerManager
from qaos.queue import QueueItem, QueueManager
from qaos.storage import create_stores


class RecordingWorker:
    def __init__(self, fail_task_id=None, error=None):
        self.calls = []
        self.fail_task_id = fail_task_id
        self.error = error or RuntimeError("retry failed")

    def execute(self, item):
        self.calls.append(item.task_id)
        item.status = "running"
        item.started = datetime.now()
        item.action.start()

        if item.task_id == self.fail_task_id:
            item.status = "failed"
            item.completed = datetime.now()
            item.action.fail()
            raise self.error

        item.action.complete()
        item.status = "completed"
        item.completed = datetime.now()
        item.result = f"Completed: {item.objective}"
        return item


class Workers:
    def __init__(self, worker):
        self.worker = worker

    def get(self, name):
        return self.worker if name == "default" else None


def build_failed_attempt(tmp_path, statuses=("completed", "failed", "pending")):
    stores = create_stores(tmp_path)
    objectives = ObjectiveManager(
        stores=stores,
        id_generator=lambda: "objective-1",
    )
    objective = objectives.create("recover work")
    objective.status = "failed"
    objectives.save()

    task_ids = iter(("task-1", "task-2", "task-3"))
    planner = PlannerManager(
        stores=stores,
        task_id_generator=lambda: next(task_ids),
    )
    plan = planner.create(objective)
    tasks = [plan.add_task(f"work {index}") for index in range(3)]
    planner.save()

    queue = QueueManager(stores=stores)
    for task, status in zip(tasks, statuses):
        task.status = status
        item = QueueItem(objective, "default", task)
        item.status = status
        queue.add(item)
    planner.save()

    return stores


def recovery_managers(stores, worker):
    objectives = ObjectiveManager(stores=stores)
    planner = PlannerManager(stores=stores)
    queue = QueueManager(stores=stores, workers=Workers(worker))
    engine = ExecutionEngine(planner=planner, queue=queue)
    registry = ExecutionRegistry()
    registry.register("default", engine)
    manager = ExecutionManager(registry=registry, objectives=objectives)
    return objectives, planner, queue, manager


def test_recovery_after_independent_reload_is_ordered_and_durable(tmp_path):
    stores = build_failed_attempt(tmp_path)
    worker = RecordingWorker()
    objectives, planner, queue, manager = recovery_managers(stores, worker)

    assert queue.items()[1].action is not planner.get_by_objective_id(
        "objective-1"
    ).tasks[1]

    recovered = manager.recover("objective-1")

    assert worker.calls == ["task-2", "task-3"]
    assert [item.task_id for item in recovered] == ["task-2", "task-3"]
    assert [item.status for item in queue.items()] == [
        "completed", "completed", "completed"
    ]
    assert [task.status for task in planner.get_by_objective_id(
        "objective-1"
    ).tasks] == ["completed", "completed", "completed"]
    assert objectives.get_by_id("objective-1").status == "completed"

    assert [item["status"] for item in stores.queue_db.load()] == [
        "completed", "completed", "completed"
    ]
    assert [task["status"] for task in stores.plan_db.load()[0]["tasks"]] == [
        "completed", "completed", "completed"
    ]
    assert stores.objective_db.load()[0]["status"] == "completed"


def test_ordinary_processing_skips_failed_attempt_but_runs_unrelated(tmp_path):
    stores = build_failed_attempt(tmp_path)
    queue = QueueManager(stores=stores)
    unrelated = QueueItem(
        "other work",
        "default",
        action=queue.items()[2].action.__class__("other", task_id="other-task"),
        objective_id="objective-2",
    )
    queue.add(unrelated)
    worker = RecordingWorker()
    reloaded = QueueManager(stores=stores, workers=Workers(worker))

    reloaded.process()

    assert worker.calls == ["other-task"]
    assert reloaded.items()[2].status == "pending"
    assert reloaded.items()[3].status == "completed"


@pytest.mark.parametrize(
    "statuses, message",
    [
        (("failed", "failed", "pending"), "exactly one failed"),
        (("pending", "failed", "completed"), "precedes"),
        (("completed", "running", "pending"), "stable"),
    ],
)
def test_queue_preflight_rejects_invalid_shapes_without_mutation(
    tmp_path, statuses, message
):
    stores = build_failed_attempt(tmp_path, statuses=statuses)
    queue = QueueManager(stores=stores)
    before = stores.queue_db.load()

    with pytest.raises(ValueError, match=message):
        queue.validate_recovery("objective-1")

    assert stores.queue_db.load() == before


def test_plan_queue_mismatch_fails_before_objective_mutation(tmp_path):
    stores = build_failed_attempt(tmp_path)
    plan_data = stores.plan_db.load()
    plan_data[0]["tasks"][1]["status"] = "completed"
    stores.plan_db.save(plan_data)
    objectives, _planner, _queue, manager = recovery_managers(
        stores, RecordingWorker()
    )

    with pytest.raises(ValueError, match="statuses do not match"):
        manager.recover("objective-1")

    assert objectives.get_by_id("objective-1").status == "failed"
    assert stores.objective_db.load()[0]["status"] == "failed"


def test_unknown_nonfailed_and_legacy_recovery_fail_closed(tmp_path):
    stores = build_failed_attempt(tmp_path)
    objectives, _planner, queue, manager = recovery_managers(
        stores, RecordingWorker()
    )

    with pytest.raises(ValueError, match="not found"):
        manager.recover("missing")

    objective = objectives.get_by_id("objective-1")
    objective.status = "completed"
    objectives.save()
    with pytest.raises(ValueError, match="only a failed"):
        manager.recover("objective-1")

    with pytest.raises(ValueError, match="no QueueItems"):
        queue.validate_recovery("legacy-id")


def test_repeated_failure_preserves_exception_and_coherent_state(tmp_path):
    stores = build_failed_attempt(tmp_path)
    original = RuntimeError("same failure")
    worker = RecordingWorker(fail_task_id="task-2", error=original)
    objectives, planner, queue, manager = recovery_managers(stores, worker)

    with pytest.raises(RuntimeError) as raised:
        manager.recover("objective-1")

    assert raised.value is original
    assert worker.calls == ["task-2"]
    assert objectives.get_by_id("objective-1").status == "failed"
    assert [item.status for item in queue.items()] == [
        "completed", "failed", "pending"
    ]
    assert [task.status for task in planner.get_by_objective_id(
        "objective-1"
    ).tasks] == ["completed", "failed", "pending"]
    assert [item["status"] for item in stores.queue_db.load()] == [
        "completed", "failed", "pending"
    ]
    assert [task["status"] for task in stores.plan_db.load()[0]["tasks"]] == [
        "completed", "failed", "pending"
    ]


def test_worker_failure_is_not_masked_by_cleanup_persistence_failure(tmp_path):
    stores = build_failed_attempt(tmp_path)
    original = RuntimeError("original worker failure")
    worker = RecordingWorker(fail_task_id="task-2", error=original)
    objectives, planner, queue, manager = recovery_managers(stores, worker)
    queue._save = lambda: (_ for _ in ()).throw(RuntimeError("queue save failed"))
    planner.save = lambda: (_ for _ in ()).throw(RuntimeError("plan save failed"))
    objectives.fail = lambda objective: (_ for _ in ()).throw(
        RuntimeError("objective save failed")
    )

    with pytest.raises(RuntimeError) as raised:
        manager.recover("objective-1")

    assert raised.value is original
