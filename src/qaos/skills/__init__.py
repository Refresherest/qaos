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


def hello():

    print("Hello from QAOS Skill")


register(
    Skill(
        "hello",
        "Demo QAOS skill",
        hello,
    )
)


__all__ = [
    "Skill",
    "SkillManager",
    "skill_manager",
    "register",
    "get",
    "all",
]