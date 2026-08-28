"""Tests for explicit skill-to-capability composition."""

from __future__ import annotations

import qaos.capabilities.manager as manager_module
import qaos.skills.skill as skill_module
from qaos.capabilities.manager import CapabilityManager
from qaos.capabilities.registry import CapabilityRegistry
from qaos.queue import QueueItem
from qaos.skills import Skill


def test_explicit_skill_uses_selected_capability(capsys) -> None:
    calls = []

    class Capability:
        name = "selected"

        def execute(self, item):
            calls.append(item)
            item.result = "selected capability"
            return item

    capabilities = CapabilityManager(registry=CapabilityRegistry())
    capabilities.register(Capability())
    skill = Skill(
        "isolated",
        capability="selected",
        capabilities=capabilities,
    )
    item = QueueItem("isolated capability objective", "selected skill")

    result = skill.execute(item)

    assert result is item
    assert calls == [item]
    assert item.result == "selected capability"
    assert capsys.readouterr().out == (
        "[Skill:isolated] Executing 'isolated capability objective'\n"
    )


def test_default_skill_capability_constructors_retain_default_services(
    monkeypatch,
) -> None:
    default_registry = object()
    default_capabilities = object()
    monkeypatch.setattr(manager_module, "capability_registry", default_registry)
    monkeypatch.setattr(skill_module, "capability_manager", default_capabilities)

    manager = CapabilityManager()
    skill = Skill("default-compatible", capability="system")

    assert manager._registry is default_registry
    assert skill._capabilities is default_capabilities


def test_explicit_capability_registries_are_isolated() -> None:
    first = CapabilityRegistry()
    second = CapabilityRegistry()
    capability = type("Capability", (), {"name": "isolated"})()

    first.register(capability)

    assert first.get(capability.name) is capability
    assert second.get(capability.name) is None
