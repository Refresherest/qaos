"""Focused tests for manager-owned Objective persistence."""

from qaos.objectives import Objective, ObjectiveManager
from qaos.storage import create_stores


def test_objective_entity_transition_does_not_persist_by_itself(tmp_path):
    stores = create_stores(tmp_path)
    manager = ObjectiveManager(stores=stores)
    objective = manager.create("state-only transition")
    persisted_before = stores.objective_db.load()

    objective.complete()

    assert objective.status == "completed"
    assert stores.objective_db.load() == persisted_before


def test_isolated_manager_owns_objective_lifecycle_persistence(tmp_path):
    first_stores = create_stores(tmp_path / "first")
    second_stores = create_stores(tmp_path / "second")
    first = ObjectiveManager(stores=first_stores)
    second = ObjectiveManager(stores=second_stores)
    completed = first.create("completed objective")
    failed = second.create("failed objective")

    first.start(completed)
    first.complete(completed)
    second.start(failed)
    second.fail(failed)

    first_data = first_stores.objective_db.load()
    second_data = second_stores.objective_db.load()

    assert first_data[0]["status"] == "completed"
    assert first_data[0]["started"] is not None
    assert first_data[0]["completed"] is not None
    assert second_data[0]["status"] == "failed"
    assert second_data[0]["started"] is not None
    assert second_data[0]["completed"] is not None
    assert [item["goal"] for item in first_data] == ["completed objective"]
    assert [item["goal"] for item in second_data] == ["failed objective"]
