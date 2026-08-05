"""
QAOS Skills
"""

from .skill import Skill
from .manager import (
    SkillManager,
    skill_manager,
)

from .registry import (
    register,
    get,
    all,
)

from qaos.actions import Action


def hello():

    print("Hello from QAOS Skill")


class ValidateArchitectureSkill(Skill):

    def __init__(self):

        super().__init__(
            name="validate_architecture",
            description="Validate system architecture",
            category="architecture",
        )

    def actions(self, objective):

        return [

            Action(
                "validate_architecture",
                "filesystem",
                "write",
                "architecture_report.txt",
                f"Architecture review for: {objective}",
                creator="AI Chief Technology Officer",
                priority="high",
                description="Generate architecture review",
            )

        ]


register(

    Skill(
        "hello",
        "Demo QAOS skill",
        hello,
    )

)

register(

    ValidateArchitectureSkill()

)

__all__ = [
    "Skill",
    "SkillManager",
    "skill_manager",
    "register",
    "get",
    "all",
]