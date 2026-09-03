"""Explicit routing must never depend on registration order or descriptions."""

from types import SimpleNamespace

import pytest

from qaos.agents import Agent
from qaos.planner import PythonFileIntent, Task
from qaos.queue import QueueItem
from qaos.skills.registry import SkillRegistry
from qaos.skills.resolver import SkillResolver


def item(executable=False):
    intent = PythonFileIntent("built.py", "print('ok')\n", "ok\n") if executable else None
    return QueueItem("misleading python_file objective", "default",
                     action=Task("misleading ordinary description", intent=intent))


def registry(names):
    result = SkillRegistry()
    for name in names:
        result.register(SimpleNamespace(name=name))
    return result


@pytest.mark.parametrize("names", [("ordinary", "builder"), ("builder", "ordinary")])
def test_exact_routes_ignore_registration_order(names):
    skills = registry(names)
    resolver = SkillResolver(skills, routes={"python_file": "builder"}, default_skill="ordinary")
    assert resolver.resolve(item()) is skills.get("ordinary")
    assert resolver.resolve(item(True)) is skills.get("builder")
    assert resolver.resolve(QueueItem("no task", "default")) is skills.get("ordinary")


def test_routes_are_copied_and_immutable():
    routes = {"python_file": "builder"}
    skills = registry(["ordinary", "builder"])
    resolver = SkillResolver(skills, routes=routes, default_skill="ordinary")
    routes["python_file"] = "ordinary"
    assert resolver.resolve(item(True)) is skills.get("builder")
    with pytest.raises(TypeError):
        resolver._routes["python_file"] = "ordinary"


@pytest.mark.parametrize("routes,default,executable", [
    ({}, None, False), ({}, "ordinary", True),
    ({"python_file": "missing"}, "ordinary", True),
    ({}, "missing", False),
])
def test_missing_configuration_fails_before_skill_execution(routes, default, executable):
    skills = registry(["ordinary"])
    calls = []
    skills.get("ordinary").execute = lambda value: calls.append(value)
    agent = Agent("test", resolver=SkillResolver(skills, routes=routes, default_skill=default))
    with pytest.raises(RuntimeError):
        agent.execute(item(executable))
    assert calls == []


def test_unknown_intent_cannot_fall_back_even_with_matching_route():
    value = item()
    value.action.intent = SimpleNamespace(type="unknown", version=1)
    resolver = SkillResolver(registry(["ordinary"]), routes={"unknown": "ordinary"}, default_skill="ordinary")
    with pytest.raises(ValueError, match="Unsupported"):
        resolver.resolve(value)


def test_non_task_action_rejected_in_explicit_mode():
    value = QueueItem("legacy", "default", action=SimpleNamespace())
    with pytest.raises(TypeError):
        SkillResolver(registry(["ordinary"]), routes={}, default_skill="ordinary").resolve(value)


def test_legacy_mode_retains_first_registered_behavior():
    skills = registry(["first", "second"])
    resolver = SkillResolver(skills)
    assert resolver.resolve(item()) is skills.get("first")
    assert resolver.resolve(item(True)) is skills.get("first")
    with pytest.raises(RuntimeError, match="No skills"):
        SkillResolver(SkillRegistry()).resolve(item())


@pytest.mark.parametrize("routes,default", [([], None), ({"": "a"}, None),
    ({"python_file": 1}, None), ({}, ""), (None, "ordinary")])
def test_invalid_configuration_rejected(routes, default):
    with pytest.raises((TypeError, ValueError)):
        SkillResolver(routes=routes, default_skill=default)
