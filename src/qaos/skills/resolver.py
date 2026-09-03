"""
QAOS Skill Resolver
"""

from collections.abc import Mapping
from types import MappingProxyType

from qaos.planner.task import Task
from qaos.planner.intents import PythonFileIntent
from .registry import skill_registry


class SkillResolver:
    """
    Resolves the most appropriate
    skill for an incoming QueueItem.

    Explicit routes select exact typed intent or an explicit default.
    Construction without routes preserves first-registered compatibility.
    """

    def __init__(self, registry=None, *, routes=None, default_skill=None):
        self._registry = skill_registry if registry is None else registry
        if routes is None and default_skill is not None:
            raise ValueError("default_skill requires explicit routes")
        if routes is not None:
            if not isinstance(routes, Mapping):
                raise TypeError("routes must be a mapping")
            routes = dict(routes)
            if any(
                not isinstance(value, str) or not value.strip()
                for pair in routes.items() for value in pair
            ):
                raise ValueError("route types and skill names must be non-blank strings")
        if default_skill is not None and (
            not isinstance(default_skill, str) or not default_skill.strip()
        ):
            raise ValueError("default_skill must be a non-blank string")
        self._routes = None if routes is None else MappingProxyType(routes)
        self._default_skill = default_skill

    def resolve(self, item):

        if self._routes is not None:
            return self._resolve_explicit(item)

        skills = self._registry.all()

        if not skills:

            raise RuntimeError(
                "No skills registered."
            )

        return next(
            iter(skills.values())
        )

    def _resolve_explicit(self, item):
        action = item.action
        if action is not None and not isinstance(action, Task):
            raise TypeError("explicit routing requires a Task or no action")
        intent = None if action is None else action.intent
        if intent is None:
            name = self._default_skill
            if name is None:
                raise RuntimeError("No explicit default skill configured.")
        else:
            if (
                type(intent) is not PythonFileIntent
                or intent.type != "python_file"
                or intent.version != 1
            ):
                raise ValueError("Unsupported executable intent for skill routing.")
            name = self._routes.get(intent.type)
            if name is None:
                raise RuntimeError("No explicit skill route for intent.")
        skill = self._registry.get(name)
        if skill is None:
            raise RuntimeError("Explicitly routed skill is not registered.")
        return skill


skill_resolver = SkillResolver()
