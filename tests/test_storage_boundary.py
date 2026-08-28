"""Tests for the explicit create_stores(data_dir) construction boundary.

These tests verify that storage construction is explicit (driven by
``create_stores``) and isolated to a caller-supplied temporary directory,
so the active data directory is never mutated by the test suite.
"""

from __future__ import annotations

from qaos.storage import Stores, create_stores


def test_create_stores_returns_storage_collection(tmp_path) -> None:
    stores = create_stores(tmp_path)

    assert isinstance(stores, Stores)
    assert stores.data_dir == tmp_path

    for name in (
        "memory_db",
        "knowledge_db",
        "artifact_db",
        "objective_db",
        "reflection_db",
        "event_db",
        "plan_db",
        "queue_db",
    ):
        assert hasattr(stores, name)


def test_create_stores_isolates_each_store_to_data_dir(tmp_path) -> None:
    stores = create_stores(tmp_path)

    stores.memory_db.save([{"title": "isolated"}])

    assert stores.memory_db.load() == [{"title": "isolated"}]
    assert (tmp_path / "memory.json").exists()

    # sibling stores in the same collection remain empty/uncreated
    assert stores.knowledge_db.load() == []
    assert not (tmp_path / "knowledge.json").exists()


def test_create_stores_does_not_touch_active_data_dir(tmp_path) -> None:
    from qaos.storage import paths

    active = paths.DATA
    active_queue = active / "queue.json"
    active_before = (
        (
            active_queue.read_bytes(),
            active_queue.stat().st_mtime_ns,
        )
        if active_queue.exists()
        else None
    )

    stores = create_stores(tmp_path)

    stores.queue_db.save([{"objective": "x", "assignee": "y", "status": "pending"}])

    # the isolated write landed in the temporary directory only
    assert (tmp_path / "queue.json").exists()
    if active_before is None:
        assert not active_queue.exists()
    else:
        assert (
            active_queue.read_bytes(),
            active_queue.stat().st_mtime_ns,
        ) == active_before


def test_storage_no_longer_exposes_module_level_db_singletons() -> None:
    import qaos.storage as storage

    # construction is explicit via create_stores, not module-level singletons
    assert hasattr(storage, "create_stores")
    assert hasattr(storage, "Stores")

    for name in (
        "memory_db",
        "knowledge_db",
        "artifact_db",
        "objective_db",
        "reflection_db",
        "event_db",
        "plan_db",
        "queue_db",
    ):
        assert not hasattr(storage, name)


def test_manager_accepts_explicit_stores(tmp_path) -> None:
    from qaos.memory.manager import MemoryManager

    stores = create_stores(tmp_path)

    manager = MemoryManager(stores=stores)

    manager.create("alpha", "content")

    # persisted through the isolated collection, not the active data dir
    assert (tmp_path / "memory.json").exists()
    assert stores.memory_db.load()[0]["title"] == "alpha"


def test_explicit_memory_managers_have_isolated_registries(tmp_path) -> None:
    from qaos.memory.manager import MemoryManager

    first_stores = create_stores(tmp_path / "first")
    second_stores = create_stores(tmp_path / "second")

    first = MemoryManager(stores=first_stores)
    second = MemoryManager(stores=second_stores)

    first.create("first", "one")
    second.create("second", "two")

    assert [item["title"] for item in first_stores.memory_db.load()] == ["first"]
    assert [item["title"] for item in second_stores.memory_db.load()] == ["second"]
    assert first.get("second") is None
    assert second.get("first") is None


def test_memory_registry_compatibility_functions_use_default_registry() -> None:
    from qaos.memory import registry
    from qaos.memory.memory import Memory

    memory = Memory("compatibility", "default registry")
    previous = registry.all().get(memory.title)

    registry.register(memory)
    try:
        assert registry.get(memory) is memory
        assert registry.all()["compatibility"] is memory
    finally:
        if previous is None:
            registry.unregister(memory)
        else:
            registry.register(previous)


def test_memory_manager_string_identity_lifecycle_after_reload(tmp_path) -> None:
    from qaos.memory.manager import MemoryManager

    stores = create_stores(tmp_path / "memory-identity")
    manager = MemoryManager(stores=stores)
    memory = manager.create("persistent memory identity", "content")

    assert manager.get(memory.title) is memory
    assert manager.get(memory) is memory

    reloaded = MemoryManager(stores=stores)

    assert reloaded.get(memory.title).title == memory.title

    reloaded.unregister(memory.title)

    assert reloaded.get(memory.title) is None
    assert stores.memory_db.load() == []


def test_explicit_artifact_managers_have_isolated_registries(tmp_path) -> None:
    from qaos.artifacts.manager import ArtifactManager

    first_stores = create_stores(tmp_path / "first-artifacts")
    second_stores = create_stores(tmp_path / "second-artifacts")

    first = ArtifactManager(stores=first_stores)
    second = ArtifactManager(stores=second_stores)

    first_artifact = first.create(
        "first",
        "draft",
        "test",
        "objective-one",
        "one",
    )
    second_artifact = second.create(
        "second",
        "draft",
        "test",
        "objective-two",
        "two",
    )

    assert [item["title"] for item in first_stores.artifact_db.load()] == ["first"]
    assert [item["title"] for item in second_stores.artifact_db.load()] == ["second"]
    assert first.get(first_artifact) is first_artifact
    assert second.get(second_artifact) is second_artifact
    assert first.get(second_artifact) is None
    assert second.get(first_artifact) is None


def test_artifact_registry_compatibility_functions_use_default_registry() -> None:
    from qaos.artifacts import registry
    from qaos.artifacts.artifact import Artifact

    artifact = Artifact(
        "compatibility-artifact",
        "test",
        "test",
        "test-objective",
        "content",
    )
    previous = registry.all().get(artifact.title)

    registry.register(artifact)
    try:
        assert registry.get(artifact) is artifact
        assert registry.all()[artifact.title] is artifact
    finally:
        if previous is None:
            registry.all().pop(artifact.title, None)
        else:
            registry.register(previous)


def test_artifact_manager_resolves_string_identity_after_reload(tmp_path) -> None:
    from qaos.artifacts.manager import ArtifactManager

    stores = create_stores(tmp_path / "artifact-identity")
    manager = ArtifactManager(stores=stores)
    artifact = manager.create(
        "persistent artifact identity",
        "draft",
        "test",
        "test objective",
        "content",
    )

    assert manager.get(artifact.title) is artifact
    assert manager.get(artifact) is artifact

    reloaded = ArtifactManager(stores=stores)

    assert reloaded.get(artifact.title).title == artifact.title


def test_explicit_objective_managers_have_isolated_registries(tmp_path) -> None:
    from qaos.objectives.manager import ObjectiveManager

    first_stores = create_stores(tmp_path / "first-objectives")
    second_stores = create_stores(tmp_path / "second-objectives")

    first = ObjectiveManager(stores=first_stores)
    second = ObjectiveManager(stores=second_stores)

    first_objective = first.create("first objective")
    second_objective = second.create("second objective")

    assert [item["goal"] for item in first_stores.objective_db.load()] == [
        "first objective"
    ]
    assert [item["goal"] for item in second_stores.objective_db.load()] == [
        "second objective"
    ]
    assert first.get(first_objective) is first_objective
    assert second.get(second_objective) is second_objective
    assert first.get(second_objective) is None
    assert second.get(first_objective) is None


def test_objective_registry_compatibility_functions_use_default_registry() -> None:
    from qaos.objectives import registry
    from qaos.objectives.objective import Objective

    objective = Objective("compatibility objective")
    previous = registry.all().get(objective.goal)

    registry.register(objective)
    try:
        assert registry.get(objective) is objective
        assert registry.all()[objective.goal] is objective
    finally:
        if previous is None:
            registry.unregister(objective)
        else:
            registry.register(previous)


def test_explicit_planner_managers_have_isolated_registries(tmp_path) -> None:
    from qaos.objectives.objective import Objective
    from qaos.planner.manager import PlannerManager

    first_stores = create_stores(tmp_path / "first-plans")
    second_stores = create_stores(tmp_path / "second-plans")

    first = PlannerManager(stores=first_stores)
    second = PlannerManager(stores=second_stores)

    first_objective = Objective("first plan objective")
    second_objective = Objective("second plan objective")
    first_plan = first.create(first_objective)
    second_plan = second.create(second_objective)

    assert [item["objective"] for item in first_stores.plan_db.load()] == [
        "first plan objective"
    ]
    assert [item["objective"] for item in second_stores.plan_db.load()] == [
        "second plan objective"
    ]
    assert first.get(first_objective) is first_plan
    assert second.get(second_objective) is second_plan
    assert first.get(second_objective) is None
    assert second.get(first_objective) is None


def test_plan_registry_compatibility_functions_use_default_registry() -> None:
    from qaos.objectives.objective import Objective
    from qaos.planner import registry
    from qaos.planner.plan import Plan

    objective = Objective("compatibility plan objective")
    plan = Plan(objective)
    previous = registry.all().get(objective.goal)

    registry.register(plan)
    try:
        assert registry.get(objective) is plan
        assert registry.all()[objective.goal] is plan
    finally:
        if previous is None:
            registry.unregister(objective)
        else:
            registry.register(previous)


def test_explicit_queue_managers_have_isolated_registries(tmp_path) -> None:
    from qaos.queue import QueueItem, QueueManager

    first_stores = create_stores(tmp_path / "first-queue")
    second_stores = create_stores(tmp_path / "second-queue")

    first = QueueManager(stores=first_stores)
    second = QueueManager(stores=second_stores)

    first.add(QueueItem("first objective", "first assignee"))
    second.add(QueueItem("second objective", "second assignee"))

    assert [item["objective"] for item in first_stores.queue_db.load()] == [
        "first objective"
    ]
    assert [item["objective"] for item in second_stores.queue_db.load()] == [
        "second objective"
    ]
    assert [item.objective for item in first.items()] == ["first objective"]
    assert [item.objective for item in second.items()] == ["second objective"]


def test_queue_registry_compatibility_functions_use_default_registry() -> None:
    from qaos.queue import QueueItem
    from qaos.queue import registry

    previous = registry.all()
    item = QueueItem("compatibility queue objective", "compatibility assignee")

    registry.clear()
    registry.add(item)
    try:
        assert registry.all() == [item]
    finally:
        registry.clear()
        for previous_item in previous:
            registry.add(previous_item)
