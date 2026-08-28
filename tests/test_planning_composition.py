"""Tests for explicit planning-stage composition."""

from __future__ import annotations

import importlib

from qaos.artifacts.manager import ArtifactManager
from qaos.context.manager import ContextManager
from qaos.knowledge.manager import KnowledgeManager
from qaos.memory.manager import MemoryManager
from qaos.objectives.objective import Objective
from qaos.planner.generator import PlanGenerator
from qaos.planner.manager import PlannerManager
from qaos.retrieval.engine import RetrievalEngine
from qaos.retrieval.manager import RetrievalManager
from qaos.storage import create_stores


def test_explicit_planning_chain_uses_selected_workspace(tmp_path) -> None:
    stores = create_stores(tmp_path / "planning")
    goal = "isolated planning objective"
    MemoryManager(stores=stores).create(goal, "memory")
    KnowledgeManager(stores=stores).create("knowledge", "general", goal)
    ArtifactManager(stores=stores).create(
        "artifact", "text", "test", goal, goal
    )
    context = ContextManager(
        retrieval=RetrievalManager(
            engine=RetrievalEngine(
                memory=MemoryManager(stores=stores),
                knowledge=KnowledgeManager(stores=stores),
                artifacts=ArtifactManager(stores=stores),
            )
        )
    )
    manager = PlannerManager(
        stores=stores,
        generator=PlanGenerator(context=context),
    )
    objective = Objective(goal)

    plan = manager.plan(objective)

    assert [task.description for task in plan.tasks[:3]] == [
        "Review existing knowledge",
        "Review previous experience",
        "Review existing artifacts",
    ]
    assert context.get(goal).objective is objective
    assert manager.get(goal) is plan
    assert [item["objective"] for item in stores.plan_db.load()] == [goal]


def test_default_planning_constructors_retain_default_services(
    monkeypatch, tmp_path
) -> None:
    retrieval_engine_module = importlib.import_module("qaos.retrieval.engine")
    retrieval_manager_module = importlib.import_module("qaos.retrieval.manager")
    context_manager_module = importlib.import_module("qaos.context.manager")
    generator_module = importlib.import_module("qaos.planner.generator")
    planner_manager_module = importlib.import_module("qaos.planner.manager")
    default_memory = object()
    default_knowledge = object()
    default_artifacts = object()
    default_engine = object()
    default_retrieval = object()
    default_context = object()
    default_generator = object()
    monkeypatch.setattr(retrieval_engine_module, "memory_manager", default_memory)
    monkeypatch.setattr(
        retrieval_engine_module, "knowledge_manager", default_knowledge
    )
    monkeypatch.setattr(
        retrieval_engine_module, "artifact_manager", default_artifacts
    )
    monkeypatch.setattr(retrieval_manager_module, "retrieval_engine", default_engine)
    monkeypatch.setattr(context_manager_module, "retrieval_manager", default_retrieval)
    monkeypatch.setattr(generator_module, "context_manager", default_context)
    monkeypatch.setattr(planner_manager_module, "plan_generator", default_generator)

    engine = RetrievalEngine()
    retrieval = RetrievalManager()
    context = ContextManager()
    generator = PlanGenerator()
    manager = PlannerManager(stores=create_stores(tmp_path / "default-services"))

    assert engine._memory is default_memory
    assert engine._knowledge is default_knowledge
    assert engine._artifacts is default_artifacts
    assert retrieval._engine is default_engine
    assert context._retrieval is default_retrieval
    assert generator._context is default_context
    assert manager._generator is default_generator


def test_explicit_context_managers_have_isolated_registries() -> None:
    class Retrieval:
        def search(self, query):
            return {"memory": [], "knowledge": [], "artifacts": []}

    first = ContextManager(retrieval=Retrieval())
    second = ContextManager(retrieval=Retrieval())
    objective = Objective("private planning context")

    created = first.create(objective)

    assert first.get(objective.goal) is created
    assert second.get(objective.goal) is None
