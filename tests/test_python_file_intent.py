"""Acceptance tests for OWNER-DECISION-021."""

from pathlib import Path
import subprocess

import pytest

from qaos.agents import Agent
from qaos.agents.manager import AgentManager
from qaos.agents.registry import AgentRegistry
from qaos.capabilities import CapabilityManager, PythonFileCapability
from qaos.capabilities.registry import CapabilityRegistry
from qaos.execution.engine import ExecutionEngine
from qaos.execution.manager import ExecutionManager
from qaos.execution.registry import ExecutionRegistry
from qaos.objectives import ObjectiveManager
from qaos.planner import PlannerManager, PythonFileIntent, Task
from qaos.queue import QueueManager
from qaos.skills import Skill
from qaos.skills.manager import SkillManager
from qaos.skills.registry import SkillRegistry
from qaos.skills.resolver import SkillResolver
from qaos.storage import create_stores
from qaos.workers.default import DefaultWorker
from qaos.workers.manager import WorkerManager
from qaos.workers.registry import WorkerRegistry


def execution(workspace):
    stores = create_stores(workspace / "state")
    objectives = ObjectiveManager(stores=stores, id_generator=lambda: "objective-1")
    planner = PlannerManager(stores=stores, task_id_generator=lambda: "task-1")

    capabilities = CapabilityManager(registry=CapabilityRegistry())
    capabilities.register(PythonFileCapability(workspace))
    skills = SkillRegistry()
    SkillManager(registry=skills).register(
        Skill("python-file", "python_file", capabilities=capabilities)
    )
    agents = AgentManager(registry=AgentRegistry())
    agents.register(Agent("default", resolver=SkillResolver(registry=skills)))
    queue = QueueManager(
        stores=stores,
        workers=WorkerManager(
            registry=WorkerRegistry(), default=DefaultWorker(agents=agents)
        ),
    )
    engines = ExecutionRegistry()
    engines.register("default", ExecutionEngine(planner=planner, queue=queue))
    return stores, objectives, planner, queue, ExecutionManager(
        registry=engines, objectives=objectives
    )


def add_intent(objectives, planner, *, source="print('QAOS built this')\n",
               expected="QAOS built this\n", path="built.py"):
    objective = objectives.create("Build one deterministic program")
    plan = planner.create(objective)
    plan.add_task(Task(
        "Build and verify one Python file",
        intent=PythonFileIntent(path, source, expected),
    ))
    planner.save()
    return objective


def test_executes_persists_and_verifies_one_file(tmp_path):
    stores, objectives, planner, queue, manager = execution(tmp_path)
    objective = add_intent(objectives, planner)

    manager.execute(objective)

    assert (tmp_path / "built.py").read_text(encoding="utf-8") == "print('QAOS built this')\n"
    assert objective.status == "completed"
    task = planner.get(objective).tasks[0]
    assert task.status == "completed"
    item = queue.items()[0]
    assert item.status == "completed"
    assert item.result["stdout"] == "QAOS built this\n"
    assert item.result["relative_path"] == "built.py"
    assert len(item.result["source_sha256"]) == 64
    assert "intent" in stores.plan_db.load()[0]["tasks"][0]
    assert "intent" in stores.queue_db.load()[0]["action"]
    reloaded = PlannerManager(stores=stores)
    assert reloaded.get_by_objective_id(objective.objective_id).tasks[0].intent == task.intent


def test_verification_failure_is_truthful_and_recovery_will_not_overwrite(tmp_path, monkeypatch):
    _stores, objectives, planner, queue, manager = execution(tmp_path)
    objective = add_intent(objectives, planner)
    monkeypatch.setattr(
        subprocess, "run",
        lambda *args, **kwargs: subprocess.CompletedProcess(args[0], 1),
    )

    with pytest.raises(RuntimeError, match="verification failed"):
        manager.execute(objective)

    assert objective.status == "failed"
    assert planner.get(objective).tasks[0].status == "failed"
    assert queue.items()[0].status == "failed"
    assert queue.items()[0].result["exit_code"] == 1
    with pytest.raises(FileExistsError, match="already exists"):
        manager.recover(objective.objective_id)
    assert objective.status == "failed"


@pytest.mark.parametrize("path", ["../escape.py", "/absolute.py", "file.txt", "missing/file.py"])
def test_rejects_unsafe_or_unapproved_targets(tmp_path, path):
    capability = PythonFileCapability(tmp_path)
    task = Task("unsafe", intent=PythonFileIntent(path, "print('x')\n", "x\n"))
    item = type("Item", (), {"action": task, "result": None})()
    with pytest.raises((ValueError, FileExistsError)):
        capability.execute(item)
    assert task.status == "failed"


def test_rejects_existing_file_and_escaping_symlink(tmp_path):
    (tmp_path / "existing.py").write_text("original", encoding="utf-8")
    capability = PythonFileCapability(tmp_path)
    task = Task("existing", intent=PythonFileIntent("existing.py", "print('x')\n", "x\n"))
    item = type("Item", (), {"action": task, "result": None})()
    with pytest.raises(FileExistsError):
        capability.execute(item)
    assert (tmp_path / "existing.py").read_text(encoding="utf-8") == "original"

    outside = tmp_path.parent / "outside-wo111"
    outside.mkdir(exist_ok=True)
    link = tmp_path / "linked"
    try:
        link.symlink_to(outside, target_is_directory=True)
    except OSError:
        pytest.skip("directory symlinks are unavailable in this environment")
    escaped = Task(
        "escape", intent=PythonFileIntent("linked/escape.py", "print('x')\n", "x\n")
    )
    with pytest.raises(ValueError, match="escapes"):
        capability.execute(type("Item", (), {"action": escaped, "result": None})())


def test_rejects_unapproved_timeout(tmp_path):
    with pytest.raises(ValueError, match="timeout_seconds"):
        PythonFileCapability(tmp_path, timeout_seconds=0)


def test_intent_validation_and_legacy_serialization():
    legacy = Task("legacy")
    assert "intent" not in legacy.to_dict()
    assert Task.from_dict(legacy.to_dict()).intent is None
    with pytest.raises(ValueError, match="unsupported"):
        Task.from_dict({"description": "x", "intent": {
            "type": "shell", "version": 1, "relative_path": "x.py",
            "source": "x", "expected_stdout": "",
        }})
    with pytest.raises(ValueError, match="non-blank"):
        PythonFileIntent("x.py", " ", "")
    with pytest.raises(ValueError, match="print-only"):
        PythonFileIntent("x.py", "import socket\n", "")
    with pytest.raises(ValueError, match="print-only"):
        PythonFileIntent("x.py", "print('x')\n", "different\n")
