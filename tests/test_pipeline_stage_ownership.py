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


def test_execution_engine_returns_report_without_reflection() -> None:
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

    report = ExecutionEngine(
        planner=Planner(),
        queue=Queue(),
    ).execute(SimpleNamespace(goal="stage boundary"))

    assert report.success is True
    assert not hasattr(report, "reflection")
    assert log.events == ["get-plan", "process-queue", "save-plan"]


def test_execution_engine_default_constructor_retains_default_managers(
    monkeypatch,
) -> None:
    default_planner = object()
    default_queue = object()
    monkeypatch.setattr(execution_engine_module, "planner_manager", default_planner)
    monkeypatch.setattr(execution_engine_module, "queue_manager", default_queue)

    engine = ExecutionEngine()

    assert engine._planner is default_planner
    assert engine._queue is default_queue


def test_pipeline_produces_one_reflection_and_one_learning_call() -> None:
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

    pipeline = ExecutivePipeline(
        classifier=Classifier(),
        council=Council(),
        planner=Planner(),
        execution=Execution(),
        reflection=Reflection(),
        learning=Learning(),
    )

    assert pipeline.execute(objective, result) is result
    assert result.reflection is reflection
    assert log.events == [
        "classify", "delegate", "plan", "execute", "reflect", "learn"
    ]


def test_pipeline_default_constructor_retains_default_managers(monkeypatch) -> None:
    defaults = {
        "classifier": object(),
        "council": object(),
        "planner": object(),
        "execution": object(),
        "reflection": object(),
        "learning": object(),
    }
    monkeypatch.setattr(pipeline_module, "classifier_manager", defaults["classifier"])
    monkeypatch.setattr(pipeline_module, "council_manager", defaults["council"])
    monkeypatch.setattr(pipeline_module, "planner_manager", defaults["planner"])
    monkeypatch.setattr(pipeline_module, "execution_manager", defaults["execution"])
    monkeypatch.setattr(pipeline_module, "reflection_manager", defaults["reflection"])
    monkeypatch.setattr(pipeline_module, "learning_manager", defaults["learning"])

    pipeline = ExecutivePipeline()

    assert pipeline._classifier is defaults["classifier"]
    assert pipeline._council is defaults["council"]
    assert pipeline._planner is defaults["planner"]
    assert pipeline._execution is defaults["execution"]
    assert pipeline._reflection is defaults["reflection"]
    assert pipeline._learning is defaults["learning"]
