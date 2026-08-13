"""Focused regression tests for ExecutivePipeline stage ownership."""

from __future__ import annotations

from types import SimpleNamespace

from qaos.execution.engine import ExecutionEngine
from qaos.executive.pipeline import ExecutivePipeline
import qaos.execution.engine as execution_engine_module
import qaos.executive.pipeline as pipeline_module


class CallLog:
    def __init__(self) -> None:
        self.events: list[str] = []


def test_execution_engine_returns_report_without_reflection(monkeypatch) -> None:
    """Execution owns only execution output, never a reflection artifact."""
    log = CallLog()
    plan = SimpleNamespace(tasks=[])

    class Planner:
        def get(self, goal):
            log.events.append("get-plan")
            return plan

        def save(self):
            log.events.append("save-plan")

    class Queue:
        def process(self):
            log.events.append("process-queue")

    monkeypatch.setattr(execution_engine_module, "planner_manager", Planner())
    monkeypatch.setattr(execution_engine_module, "queue_manager", Queue())

    report = ExecutionEngine().execute(SimpleNamespace(goal="stage boundary"))

    assert report.success is True
    assert not hasattr(report, "reflection")
    assert log.events == ["get-plan", "process-queue", "save-plan"]


def test_pipeline_produces_one_reflection_and_one_learning_call(monkeypatch) -> None:
    """Only ExecutivePipeline coordinates reflection and learning once."""
    log = CallLog()
    objective = SimpleNamespace(goal="exactly once")
    report = SimpleNamespace(success=True)
    reflection = SimpleNamespace(objective=objective)
    result = SimpleNamespace()

    class Classifier:
        def classify(self, value):
            log.events.append("classify")
            return "classification"

    class Council:
        def delegate(self, value):
            log.events.append("delegate")
            return "assignment"

    class Planner:
        def plan(self, value):
            log.events.append("plan")
            return "plan"

    class Execution:
        def execute(self, value):
            log.events.append("execute")
            return report

    class Reflection:
        def reflect(self, value, execution_report):
            assert value is objective
            assert execution_report is report
            log.events.append("reflect")
            return reflection

    class Learning:
        def learn(self, value):
            assert value is reflection
            log.events.append("learn")

    monkeypatch.setattr(pipeline_module, "classifier_manager", Classifier())
    monkeypatch.setattr(pipeline_module, "council_manager", Council())
    monkeypatch.setattr(pipeline_module, "planner_manager", Planner())
    monkeypatch.setattr(pipeline_module, "execution_manager", Execution())
    monkeypatch.setattr(pipeline_module, "reflection_manager", Reflection())
    monkeypatch.setattr(pipeline_module, "learning_manager", Learning())

    assert ExecutivePipeline().execute(objective, result) is result
    assert result.reflection is reflection
    assert log.events == [
        "classify", "delegate", "plan", "execute", "reflect", "learn"
    ]
