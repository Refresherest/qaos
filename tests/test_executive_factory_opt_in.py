"""Factory composition evidence, not an application Task-submission API."""

import pytest

from qaos.capabilities.registry import capability_registry
from qaos.executive import create_executive
from qaos.objectives import ObjectiveManager
from qaos.planner import PythonFileIntent, Task
from qaos.queue import QueueItem
from qaos.skills.registry import skill_registry
from qaos.storage import create_stores


def resolver_for(executive):
    # Inspect the factory-owned graph without adding production accessors.
    execution = executive._recovery
    queue = execution._registry.get("default")._queue
    return queue._workers.get("default")._agents.get("default")._resolver


def test_enabled_factory_is_private_and_construction_does_not_write(tmp_path):
    output = tmp_path / "output"
    output.mkdir()
    stores = create_stores(tmp_path / "state")
    global_capabilities = capability_registry.all()
    global_skills = dict(skill_registry.all())
    before = set(tmp_path.rglob("*"))
    enabled = create_executive(stores, python_file_workspace=output)
    assert set(tmp_path.rglob("*")) == before
    resolver = resolver_for(enabled)
    ordinary = QueueItem("ordinary", "default", action=Task("ordinary"))
    typed = QueueItem("typed", "default", action=Task(
        "typed", intent=PythonFileIntent("built.py", "print('ok')\n", "ok\n")
    ))
    assert resolver.resolve(ordinary).name == "planning"
    skill = resolver.resolve(typed)
    assert skill.name == "python-file"
    assert set(skill._capabilities.capabilities()) == {"system", "python_file"}
    assert skill._capabilities.get("python_file")._workspace == output.resolve()
    assert capability_registry.all() == global_capabilities
    assert skill_registry.all() == global_skills


def test_two_enabled_instances_and_default_do_not_share_authority(tmp_path):
    first, second = tmp_path / "first", tmp_path / "second"
    first.mkdir()
    second.mkdir()
    a = resolver_for(create_executive(create_stores(tmp_path / "a"), python_file_workspace=first))
    b = resolver_for(create_executive(create_stores(tmp_path / "b"), python_file_workspace=second))
    default = resolver_for(create_executive(create_stores(tmp_path / "default")))
    typed = QueueItem("typed", "default", action=Task(
        "typed", intent=PythonFileIntent("built.py", "print('ok')\n", "ok\n")
    ))
    cap_a = a.resolve(typed)._capabilities.get("python_file")
    cap_b = b.resolve(typed)._capabilities.get("python_file")
    assert cap_a is not cap_b
    assert cap_a._workspace == first.resolve()
    assert cap_b._workspace == second.resolve()
    assert default._routes is None
    assert default.resolve(typed).name == "planning"
    assert default.resolve(typed)._capabilities.get("python_file") is None


@pytest.mark.parametrize("target", ["missing", "file", "relative", "empty"])
def test_bad_output_directory_rejected_without_state_creation(tmp_path, target):
    path = tmp_path / target
    if target == "file":
        path.write_text("not a directory", encoding="utf-8")
    supplied = "relative" if target == "relative" else "" if target == "empty" else path
    stores = create_stores(tmp_path / "state")
    before = set(tmp_path.rglob("*"))
    with pytest.raises(ValueError):
        create_executive(stores, python_file_workspace=supplied)
    assert set(tmp_path.rglob("*")) == before


def test_ordinary_pipeline_still_works_when_opted_in(tmp_path):
    output = tmp_path / "output"
    output.mkdir()
    stores = create_stores(tmp_path / "state")
    objectives = ObjectiveManager(stores=stores)
    executive = create_executive(stores, objectives=objectives, python_file_workspace=output)
    objective = objectives.create("plan ordinary work")
    result = executive.execute(objective)
    assert result.completed
    assert objective.status == "completed"
    assert all(row["status"] == "completed" for row in stores.queue_db.load())
    assert list(output.iterdir()) == []
