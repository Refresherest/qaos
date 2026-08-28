"""Tests for explicit Executive entry-chain composition."""

from __future__ import annotations

import importlib
from types import SimpleNamespace

import pytest

from qaos.executive.manager import ExecutiveManager
from qaos.executive.orchestrator import ExecutiveOrchestrator


class RecordingLogger:
    def __init__(self):
        self.messages = []

    def info(self, message):
        self.messages.append(message)


def test_explicit_manager_runs_explicit_pipeline_through_orchestrator() -> None:
    objective = SimpleNamespace(goal="explicit executive composition")
    calls = []

    class Pipeline:
        def execute(self, value, result):
            calls.append((value, result))
            result.classification = "explicit"
            return result

    logger = RecordingLogger()
    manager = ExecutiveManager(
        orchestrator_service=ExecutiveOrchestrator(pipeline=Pipeline()),
        logger_service=logger,
    )

    result = manager.execute(objective)

    assert result.objective is objective
    assert result.completed is True
    assert result.classification == "explicit"
    assert len(calls) == 1
    assert logger.messages == [
        "Executive executing 'explicit executive composition'",
        "Executive execution complete.",
    ]


def test_explicit_orchestrator_preserves_pipeline_failure_semantics() -> None:
    class PipelineFailure:
        def execute(self, objective, result):
            raise RuntimeError("pipeline failed")

    orchestrator = ExecutiveOrchestrator(pipeline=PipelineFailure())

    with pytest.raises(RuntimeError, match="pipeline failed"):
        orchestrator.execute(SimpleNamespace(goal="failure"))


def test_default_executive_constructors_retain_default_services(monkeypatch) -> None:
    manager_module = importlib.import_module("qaos.executive.manager")
    orchestrator_module = importlib.import_module("qaos.executive.orchestrator")

    default_pipeline = object()
    default_orchestrator = object()
    default_logger = object()
    monkeypatch.setattr(orchestrator_module, "executive_pipeline", default_pipeline)
    monkeypatch.setattr(manager_module, "orchestrator", default_orchestrator)
    monkeypatch.setattr(manager_module, "logger", default_logger)

    constructed_orchestrator = ExecutiveOrchestrator()
    constructed_manager = ExecutiveManager()

    assert constructed_orchestrator._pipeline is default_pipeline
    assert constructed_manager._orchestrator is default_orchestrator
    assert constructed_manager._logger is default_logger
