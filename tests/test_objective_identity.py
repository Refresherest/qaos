"""Objective identity contract tests for OWNER-DECISION-013."""

import pytest

from qaos.objectives import Objective, ObjectiveManager
from qaos.storage import create_stores


def deterministic_ids(*values):
    generated = iter(values)
    return lambda: next(generated)


def test_manager_assigns_deterministic_immutable_identity(tmp_path):
    manager = ObjectiveManager(
        stores=create_stores(tmp_path),
        id_generator=deterministic_ids("objective-1"),
    )

    objective = manager.create("identified objective")
    manager.register(objective)

    assert objective.objective_id == "objective-1"
    assert manager.get_by_id("objective-1") is objective
    assert len(manager.objective_records()) == 1

    with pytest.raises(ValueError, match="immutable"):
        objective._assign_identity("objective-2")


def test_dual_indexes_preserve_equal_goal_records_and_latest_lookup(tmp_path):
    stores = create_stores(tmp_path)
    manager = ObjectiveManager(
        stores=stores,
        id_generator=deterministic_ids("objective-1", "objective-2"),
    )

    first = manager.create("repeat goal")
    second = manager.create("repeat goal")

    assert manager.get("repeat goal") is second
    assert manager.get(first) is first
    assert manager.get(second) is second
    assert manager.get_by_id("objective-1") is first
    assert manager.get_by_id("objective-2") is second
    assert manager.objective_records() == (first, second)
    assert [item["objective_id"] for item in stores.objective_db.load()] == [
        "objective-1",
        "objective-2",
    ]

    reloaded = ObjectiveManager(
        stores=stores,
        id_generator=lambda: pytest.fail("reload must not generate identity"),
    )

    assert reloaded.get("repeat goal").objective_id == "objective-2"
    assert reloaded.get_by_id("objective-1").goal == "repeat goal"
    assert reloaded.get_by_id("objective-2").goal == "repeat goal"
    assert len(reloaded.objective_records()) == 2


def test_explicit_id_lookup_never_guesses_goal_strings(tmp_path):
    manager = ObjectiveManager(
        stores=create_stores(tmp_path),
        id_generator=deterministic_ids("same-text", "other-id"),
    )
    identified = manager.create("a goal")
    goal_match = Objective("same-text")
    manager.register(goal_match)

    assert manager.get("same-text") is goal_match
    assert manager.get_by_id("same-text") is identified


def test_legacy_load_keeps_missing_identity_unassigned(tmp_path):
    stores = create_stores(tmp_path)
    legacy = {
        "goal": "legacy objective",
        "status": "pending",
        "created": "2026-08-29T00:00:00",
        "started": None,
        "completed": None,
    }
    stores.objective_db.save([legacy])
    generator_calls = []

    manager = ObjectiveManager(
        stores=stores,
        id_generator=lambda: generator_calls.append(True) or "unexpected",
    )
    objective = manager.get("legacy objective")
    manager.save()

    assert objective.objective_id is None
    assert manager.get(objective) is objective
    assert manager.get_by_id("legacy objective") is None
    assert generator_calls == []
    assert stores.objective_db.load() == [legacy]


def test_registering_new_unidentified_objective_assigns_identity(tmp_path):
    manager = ObjectiveManager(
        stores=create_stores(tmp_path),
        id_generator=deterministic_ids("registered-id"),
    )
    objective = Objective("registered objective")

    manager.register(objective)

    assert objective.objective_id == "registered-id"
    assert manager.get_by_id("registered-id") is objective


def test_duplicate_non_null_identity_fails_closed(tmp_path):
    manager = ObjectiveManager(stores=create_stores(tmp_path))
    first = Objective("first", objective_id="duplicate-id")
    second = Objective("second", objective_id="duplicate-id")

    manager.register(first)

    with pytest.raises(ValueError, match="duplicate objective_id"):
        manager.register(second)

    assert manager.get_by_id("duplicate-id") is first
    assert manager.get("second") is None


def test_duplicate_persisted_identity_fails_closed_on_load(tmp_path):
    stores = create_stores(tmp_path)
    stores.objective_db.save(
        [
            {"goal": "first", "objective_id": "duplicate-id"},
            {"goal": "second", "objective_id": "duplicate-id"},
        ]
    )

    with pytest.raises(ValueError, match="duplicate objective_id"):
        ObjectiveManager(stores=stores)
