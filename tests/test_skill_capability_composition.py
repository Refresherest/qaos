"""Tests for explicit skill-to-capability composition."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import qaos.capabilities.manager as manager_module
import qaos.skills.skill as skill_module
from qaos.capabilities.manager import CapabilityManager
from qaos.capabilities.registry import CapabilityRegistry
from qaos.queue import QueueItem
from qaos.skills import Skill


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = REPOSITORY_ROOT / "src"


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


def test_default_agent_skill_capability_chain_in_clean_process() -> None:
    code = """
from qaos.agents import agent_manager
from qaos.capabilities import capability_manager, system_capability
from qaos.planner import Task
from qaos.queue import QueueItem

task = Task("default capability task")
item = QueueItem("default capability objective", "default", action=task)
agent = agent_manager.get("default")
assert capability_manager.get("system") is system_capability
assert agent.execute(item) is task
assert task.status == "completed"
assert item.status == "pending"
"""
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(SOURCE_ROOT)

    result = subprocess.run(
        [sys.executable, "-c", code],
        cwd=REPOSITORY_ROOT,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr


def test_default_worker_completes_queue_item_lifecycle_in_clean_process() -> None:
    code = """
from qaos.planner import Task
from qaos.queue import QueueItem
from qaos.workers import default_worker

task = Task("default worker lifecycle")
item = QueueItem("default worker objective", "default", action=task)
assert default_worker.execute(item) is task
assert task.status == "completed"
assert item.status == "completed"
assert item.started is not None
assert item.completed is not None
assert item.result == "Completed: default worker objective"
"""
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(SOURCE_ROOT)

    result = subprocess.run(
        [sys.executable, "-c", code],
        cwd=REPOSITORY_ROOT,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
