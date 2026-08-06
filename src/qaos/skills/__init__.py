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
    unregister,
    get,
    all,
)

from .resolver import (
    SkillResolver,
    skill_resolver,
)

#
# Default planning skill
#

register(
    Skill(
        name="planning",
        capability="system",
    )
)

__all__ = [

    "Skill",

    "SkillManager",
    "skill_manager",

    "SkillResolver",
    "skill_resolver",

    "register",
    "unregister",
    "get",
    "all",
]