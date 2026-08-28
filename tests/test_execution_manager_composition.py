"""Tests for explicit ExecutionManager composition."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from qaos.execution.manager import ExecutionManager
from qaos.execution.registry import ExecutionRegistry


def test_explicit_execution_manager_runs_engine_before_objective_save() -> None:
    objective = SimpleNamespace(goal="explicit execution manager")
    report = object()
    calls = []

    class Engine:
        def execute(self, value):
            calls.append(("execute", value))
            return report

    class Objectives:
        def save(self):
            calls.append(("save", None))

    registry = ExecutionRegistry()
    registry.register("default", Engine())
    manager = ExecutionManager(registry=registry, objectives=Objectives())

    assert manager.execute(objective) is report
    assert calls == [("execute", objective), ("save", None)]
    assert manager.engines() is registry.all()


def test_explicit_execution_manager_requires_default_engine() -> None:
    manager = ExecutionManager(
        registry=ExecutionRegistry(),
        objectives=object(),
    )

    with pytest.raises(RuntimeError, match="No execution engine registered"):
        manager.execute(SimpleNamespace(goal="missing engine"))


def test_default_execution_manager_retains_default_services(monkeypatch) -> None:
    import importlib

    manager_module = importlib.import_module("qaos.execution.manager")
    default_registry = object()
    default_objectives = object()
    monkeypatch.setattr(manager_module, "execution_registry", default_registry)
    monkeypatch.setattr(manager_module, "objective_manager", default_objectives)

    manager = ExecutionManager()

    assert manager._registry is default_registry
    assert manager._objectives is default_objectives
