"""
QAOS Skill Manager
"""

from .registry import skill_registry


class SkillManager:

    def __init__(self, registry=None):
        self._registry = skill_registry if registry is None else registry

    def register(self, skill):

        self._registry.register(skill)

    def get(self, name):

        return self._registry.get(name)

    def skills(self):

        return self._registry.all()

    def execute(self, name, *args, **kwargs):

        skill = self._registry.get(name)

        if skill is None:
            raise ValueError(
                f"Unknown skill: {name}"
            )

        return skill.execute(
            *args,
            **kwargs,
        )


skill_manager = SkillManager()
