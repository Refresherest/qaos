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
