"""Plan and QueueItem propagation tests for OWNER-DECISION-014."""

import pytest

from qaos.application import OperationalSession
from qaos.objectives import Objective
from qaos.planner import Plan, PlannerManager
from qaos.queue import QueueItem, QueueManager
from qaos.storage import create_stores


def test_plan_captures_and_serializes_objective_identity():
    objective = Objective("identified plan", objective_id="objective-1")

    plan = Plan(objective)
    restored = Plan.from_dict(plan.to_dict())

    assert plan.objective == objective.goal
    assert plan.objective_id == objective.objective_id
    assert restored.objective == objective.goal
    assert restored.objective_id == objective.objective_id


def test_plan_registry_preserves_equal_goals_and_identity_lookup(tmp_path):
    stores = create_stores(tmp_path)
    manager = PlannerManager(stores=stores)
    first_objective = Objective("repeat goal", objective_id="objective-1")
    second_objective = Objective("repeat goal", objective_id="objective-2")

    first = manager.create(first_objective)
    second = manager.create(second_objective)

    assert manager.get("repeat goal") is second
    assert manager.get(first_objective) is first
    assert manager.get(second_objective) is second
    assert manager.get_by_objective_id("objective-1") is first
    assert manager.get_by_objective_id("objective-2") is second
    assert manager.plan_records() == (first, second)
    assert [item["objective_id"] for item in stores.plan_db.load()] == [
        "objective-1",
        "objective-2",
    ]

    reloaded = PlannerManager(stores=stores)

    assert reloaded.get(first_objective).objective_id == "objective-1"
    assert reloaded.get(second_objective).objective_id == "objective-2"
    assert len(reloaded.plan_records()) == 2


def test_duplicate_plan_objective_reference_fails_closed(tmp_path):
    manager = PlannerManager(stores=create_stores(tmp_path))
    first = Plan("first", objective_id="duplicate-id")
    second = Plan("second", objective_id="duplicate-id")

    manager.register(first)

    with pytest.raises(ValueError, match="duplicate plan objective_id"):
        manager.register(second)

    assert manager.get_by_objective_id("duplicate-id") is first
    assert manager.get("second") is None


def test_plan_id_lookup_never_guesses_goal_strings(tmp_path):
    manager = PlannerManager(stores=create_stores(tmp_path))
    identified = manager.create(Objective("a goal", objective_id="same-text"))
    goal_match = manager.create(Objective("same-text", objective_id="other-id"))

    assert manager.get("same-text") is goal_match
    assert manager.get_by_objective_id("same-text") is identified


def test_duplicate_persisted_plan_reference_fails_closed(tmp_path):
    stores = create_stores(tmp_path)
    stores.plan_db.save(
        [
            {"objective": "first", "objective_id": "duplicate-id", "tasks": []},
            {"objective": "second", "objective_id": "duplicate-id", "tasks": []},
        ]
    )

    with pytest.raises(ValueError, match="duplicate plan objective_id"):
        PlannerManager(stores=stores)


def test_legacy_plan_reference_remains_omitted(tmp_path):
    stores = create_stores(tmp_path)
    legacy = {"objective": "legacy plan", "tasks": []}
    stores.plan_db.save([legacy])

    manager = PlannerManager(stores=stores)
    plan = manager.get("legacy plan")
    manager.save()

    assert plan.objective_id is None
    assert stores.plan_db.load() == [legacy]


def test_queue_items_share_and_persist_objective_reference(tmp_path):
    stores = create_stores(tmp_path)
    manager = QueueManager(stores=stores)
    objective = Objective("queued objective", objective_id="objective-1")

    first = QueueItem(objective, "first")
    second = QueueItem(objective, "second")
    manager.add(first)
    manager.add(second)

    assert first.objective == objective.goal
    assert second.objective == objective.goal
    assert first.objective_id == "objective-1"
    assert second.objective_id == "objective-1"
    assert [item["objective_id"] for item in stores.queue_db.load()] == [
        "objective-1",
        "objective-1",
    ]

    reloaded = QueueManager(stores=stores)

    assert [item.objective_id for item in reloaded.items()] == [
        "objective-1",
        "objective-1",
    ]


def test_legacy_queue_reference_remains_omitted(tmp_path):
    stores = create_stores(tmp_path)
    legacy = {
        "objective": "legacy queue item",
        "assignee": "default",
        "action": None,
        "status": "pending",
        "result": None,
        "started": None,
        "completed": None,
    }
    stores.queue_db.save([legacy])

    manager = QueueManager(stores=stores)
    manager.save()

    assert manager.items()[0].objective_id is None
    assert stores.queue_db.load() == [legacy]


def test_operational_pipeline_propagates_one_objective_identity(tmp_path):
    stores = create_stores(tmp_path)
    result = OperationalSession(stores).execute_goal("propagated objective")
    objective_id = result.objective.objective_id

    assert objective_id is not None
    assert stores.plan_db.load()[0]["objective_id"] == objective_id
    assert {item["objective_id"] for item in stores.queue_db.load()} == {
        objective_id
    }
