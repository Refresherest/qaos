"""Tests for explicit agent-to-skill composition."""

from __future__ import annotations

import qaos.agents.agent as agent_module
import qaos.skills.manager as manager_module
import qaos.skills.resolver as resolver_module
from qaos.agents import Agent
from qaos.queue import QueueItem
from qaos.skills.manager import SkillManager
from qaos.skills.registry import SkillRegistry
from qaos.skills.resolver import SkillResolver


def test_explicit_agent_uses_selected_skill_registry(capsys) -> None:
    calls = []

    class Skill:
        name = "selected"

        def execute(self, item):
            calls.append(item)
            item.result = "selected skill"
            return item

    registry = SkillRegistry()
    SkillManager(registry=registry).register(Skill())
    agent = Agent("isolated", resolver=SkillResolver(registry=registry))
    item = QueueItem("isolated skill objective", "selected agent")

    result = agent.execute(item)

    assert result is item
    assert calls == [item]
    assert item.result == "selected skill"
    assert capsys.readouterr().out == (
        "[Agent:isolated] Processing 'isolated skill objective'\n"
    )


def test_default_agent_skill_constructors_retain_default_services(
    monkeypatch,
) -> None:
    default_resolver = object()
    default_registry = object()
    monkeypatch.setattr(agent_module, "skill_resolver", default_resolver)
    monkeypatch.setattr(manager_module, "skill_registry", default_registry)
    monkeypatch.setattr(resolver_module, "skill_registry", default_registry)

    agent = Agent("default-compatible")
    manager = SkillManager()
    resolver = SkillResolver()

    assert agent._resolver is default_resolver
    assert manager._registry is default_registry
    assert resolver._registry is default_registry


def test_explicit_skill_registries_are_isolated() -> None:
    first = SkillRegistry()
    second = SkillRegistry()
    skill = type("Skill", (), {"name": "isolated"})()

    first.register(skill)

    assert first.get(skill.name) is skill
    assert second.get(skill.name) is None
