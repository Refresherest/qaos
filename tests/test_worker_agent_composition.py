"""Tests for explicit worker-to-agent composition."""

from __future__ import annotations

import pytest

import qaos.agents.manager as agent_manager_module
import qaos.workers.default as default_worker_module
import qaos.workers.manager as worker_manager_module
from qaos.agents.manager import AgentManager
from qaos.agents.registry import AgentRegistry
from qaos.planner import Task
from qaos.queue import QueueItem, QueueManager
from qaos.storage import create_stores
from qaos.workers.default import DefaultWorker
from qaos.workers.manager import WorkerManager
from qaos.workers.registry import WorkerRegistry


def test_explicit_worker_chain_uses_selected_agent(tmp_path, capsys) -> None:
    stores = create_stores(tmp_path / "worker-agent")
    calls = []

    class Agent:
        name = "default"

        def execute(self, item):
            calls.append(item)
            item.status = "completed"
            item.result = "selected agent"
            return item

    agents = AgentManager(registry=AgentRegistry())
    agents.register(Agent())
    workers = WorkerManager(
        registry=WorkerRegistry(),
        default=DefaultWorker(agents=agents),
    )
    queue = QueueManager(stores=stores, workers=workers)
    item = QueueItem("isolated agent objective", "selected worker")
    queue.add(item)

    queue.process()

    assert calls == [item]
    assert item.result == "selected agent"
    assert stores.queue_db.load()[0]["result"] == "selected agent"
    assert capsys.readouterr().out == (
        "[Worker:default] Executing 'isolated agent objective'\n"
    )


def test_default_worker_agent_constructors_retain_default_services(
    monkeypatch,
) -> None:
    default_agent_registry = object()
    default_agents = object()
    default_worker_registry = WorkerRegistry()
    default_worker = type("Worker", (), {"name": "default"})()
    monkeypatch.setattr(
        agent_manager_module, "agent_registry", default_agent_registry
    )
    monkeypatch.setattr(default_worker_module, "agent_manager", default_agents)
    monkeypatch.setattr(
        worker_manager_module, "worker_registry", default_worker_registry
    )
    monkeypatch.setattr(worker_manager_module, "default_worker", default_worker)

    agents = AgentManager()
    worker = DefaultWorker()
    workers = WorkerManager()

    assert agents._registry is default_agent_registry
    assert worker._agents is default_agents
    assert workers._registry is default_worker_registry
    assert workers.get() is default_worker


def test_explicit_agent_and_worker_registries_are_isolated() -> None:
    first_agents = AgentRegistry()
    second_agents = AgentRegistry()
    first_workers = WorkerRegistry()
    second_workers = WorkerRegistry()
    agent = type("Agent", (), {"name": "agent"})()
    worker = type("Worker", (), {"name": "worker"})()

    first_agents.register(agent)
    first_workers.register(worker)

    assert first_agents.get(agent.name) is agent
    assert second_agents.get(agent.name) is None
    assert first_workers.get(worker.name) is worker
    assert second_workers.get(worker.name) is None


def test_worker_failure_persists_failed_item_and_preserves_pending_task(
    tmp_path,
) -> None:
    stores = create_stores(tmp_path / "worker-failure-before-task")
    failure = RuntimeError("delegated worker failure")

    class Agent:
        name = "default"

        def execute(self, item):
            raise failure

    agents = AgentManager(registry=AgentRegistry())
    agents.register(Agent())
    workers = WorkerManager(
        registry=WorkerRegistry(),
        default=DefaultWorker(agents=agents),
    )
    queue = QueueManager(stores=stores, workers=workers)
    item = QueueItem(
        "worker failure before task",
        "default",
        action=Task("never-started task"),
    )
    queue.add(item)

    with pytest.raises(RuntimeError) as caught:
        queue.process()

    assert caught.value is failure
    assert item.status == "failed"
    assert item.started is not None
    assert item.completed is not None
    assert item.action.status == "pending"
    persisted = stores.queue_db.load()[0]
    assert persisted["status"] == "failed"
    assert persisted["completed"] is not None
    assert persisted["action"]["status"] == "pending"


def test_worker_failure_fails_and_persists_started_task(tmp_path) -> None:
    stores = create_stores(tmp_path / "worker-failure-after-task-start")
    failure = RuntimeError("task execution failure")

    class Agent:
        name = "default"

        def execute(self, item):
            item.action.start()
            raise failure

    agents = AgentManager(registry=AgentRegistry())
    agents.register(Agent())
    workers = WorkerManager(
        registry=WorkerRegistry(),
        default=DefaultWorker(agents=agents),
    )
    queue = QueueManager(stores=stores, workers=workers)
    task = Task("started task")
    item = QueueItem("worker failure after task start", "default", task)
    queue.add(item)

    with pytest.raises(RuntimeError) as caught:
        queue.process()

    assert caught.value is failure
    assert item.status == "failed"
    assert task.status == "failed"
    assert task.started is not None
    assert task.completed is not None
    persisted = stores.queue_db.load()[0]
    assert persisted["status"] == "failed"
    assert persisted["action"]["status"] == "failed"
    assert persisted["action"]["completed"] is not None
