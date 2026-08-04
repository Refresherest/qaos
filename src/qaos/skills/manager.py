"""
QAOS Skill Manager
"""

from .registry import register, get, all


class SkillManager:

    def register(self, skill):

        register(skill)

    def get(self, name):

        return get(name)

    def skills(self):

        return all()

    def execute(self, name, *args, **kwargs):

        skill = get(name)

        if skill is None:
            raise ValueError(
                f"Unknown skill: {name}"
            )

        return skill.execute(
            *args,
            **kwargs,
        )


skill_manager = SkillManager()