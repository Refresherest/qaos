"""Tests for explicit council-stage composition."""

from __future__ import annotations

from types import SimpleNamespace

import qaos.council.delegator as delegator_module
import qaos.council.manager as manager_module
from qaos.council.delegator import Delegator
from qaos.council.manager import CouncilManager
from qaos.council.registry import CouncilRegistry
from qaos.objectives.manager import ObjectiveManager
from qaos.queue.manager import QueueManager
from qaos.storage import create_stores


def test_explicit_council_chain_uses_selected_workspace(tmp_path, capsys) -> None:
    stores = create_stores(tmp_path / "council")
    objectives = ObjectiveManager(stores=stores)
    queue = QueueManager(stores=stores)
    registry = CouncilRegistry()
    member = SimpleNamespace(
        name="chief_technology_officer",
        title="Isolated CTO",
    )
    registry.register(member)
    manager = CouncilManager(
        registry=registry,
        delegator_service=Delegator(
            registry=registry,
            objectives=objectives,
        ),
        queue=queue,
    )
    objective = objectives.create("isolated council objective")

    selected = manager.delegate(objective)

    assert selected is member
    assert objective.owner is member
    assert manager.members() == {member.name: member}
    assert [(item.objective, item.assignee) for item in queue.items()] == [
        (objective.goal, member.title)
    ]
    assert [item["objective"] for item in stores.queue_db.load()] == [
        objective.goal
    ]
    assert capsys.readouterr().out == "[Queue] Added objective for Isolated CTO\n"


def test_default_council_constructors_retain_default_services(monkeypatch) -> None:
    default_registry = object()
    default_objectives = object()
    default_delegator = object()
    default_queue = object()
    monkeypatch.setattr(delegator_module, "council_registry", default_registry)
    monkeypatch.setattr(delegator_module, "objective_manager", default_objectives)
    monkeypatch.setattr(manager_module, "council_registry", default_registry)
    monkeypatch.setattr(manager_module, "delegator", default_delegator)
    monkeypatch.setattr(manager_module, "queue_manager", default_queue)

    constructed_delegator = Delegator()
    manager = CouncilManager()

    assert constructed_delegator._registry is default_registry
    assert constructed_delegator._objectives is default_objectives
    assert manager._registry is default_registry
    assert manager._delegator is default_delegator
    assert manager._queue is default_queue


def test_explicit_council_registries_are_isolated() -> None:
    first = CouncilRegistry()
    second = CouncilRegistry()
    member = SimpleNamespace(name="isolated-member")

    first.register(member)

    assert first.get(member.name) is member
    assert second.get(member.name) is None
