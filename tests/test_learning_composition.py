"""Tests for explicit learning-stage composition."""

from __future__ import annotations

import importlib

from qaos.knowledge.manager import KnowledgeManager
from qaos.learning.engine import LearningEngine
from qaos.learning.learner import Learner
from qaos.learning.manager import LearningManager
from qaos.memory.manager import MemoryManager
from qaos.objectives.objective import Objective
from qaos.reflection import Reflection
from qaos.reflection.manager import ReflectionManager
from qaos.storage import create_stores


def test_explicit_learning_chain_uses_selected_workspace(tmp_path) -> None:
    stores = create_stores(tmp_path / "learning")
    manager = LearningManager(
        learner_service=Learner(
            engine=LearningEngine(
                memory=MemoryManager(stores=stores),
                knowledge=KnowledgeManager(stores=stores),
            )
        )
    )
    reflection = Reflection(
        Objective("isolated learning objective"),
        summary="summary",
        successes=["success"],
        failures=["failure"],
    )

    result = manager.learn(reflection)

    assert result == {"memory": 3, "knowledge": 1}
    assert [item["content"] for item in stores.memory_db.load()] == ["failure"]
    assert [item["content"] for item in stores.knowledge_db.load()] == ["success"]


def test_default_learning_constructors_retain_default_services(monkeypatch) -> None:
    engine_module = importlib.import_module("qaos.learning.engine")
    learner_module = importlib.import_module("qaos.learning.learner")
    manager_module = importlib.import_module("qaos.learning.manager")
    default_memory = object()
    default_knowledge = object()
    default_engine = object()
    default_learner = object()
    monkeypatch.setattr(engine_module, "memory_manager", default_memory)
    monkeypatch.setattr(engine_module, "knowledge_manager", default_knowledge)
    monkeypatch.setattr(learner_module, "learning_engine", default_engine)
    monkeypatch.setattr(manager_module, "learner", default_learner)

    engine = LearningEngine()
    constructed_learner = Learner()
    manager = LearningManager()

    assert engine._memory is default_memory
    assert engine._knowledge is default_knowledge
    assert constructed_learner._engine is default_engine
    assert manager._learner is default_learner


def test_learner_accepts_reloaded_reflection_string_identity(tmp_path, capsys) -> None:
    stores = create_stores(tmp_path / "reloaded-reflection")
    objective = Objective("persisted reflection identity")
    ReflectionManager(stores=stores).create(objective, summary="summary")
    reloaded = ReflectionManager(stores=stores).get(objective.goal)
    received = []

    class Engine:
        def learn(self, reflection):
            received.append(reflection)
            return "learned"

    result = Learner(engine=Engine()).learn(reloaded)

    assert result == "learned"
    assert received == [reloaded]
    assert reloaded.objective == objective.goal
    assert capsys.readouterr().out == (
        "[Learner] Learning from persisted reflection identity\n"
    )
