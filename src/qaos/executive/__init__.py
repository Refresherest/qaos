"""
QAOS Executive Profiles
"""

from .profile import ExecutiveProfile
from .manager import (
    ExecutiveManager,
    executive_manager,
)
from .registry import (
    register,
    get,
    all,
)

#
# Chief of Staff Profile
#

chief_of_staff = ExecutiveProfile(
    "AI Chief of Staff"
)

chief_of_staff.add_skill(
    "analyze_objective"
)

chief_of_staff.add_skill(
    "delegate_work"
)

chief_of_staff.add_skill(
    "review_plan"
)

register(chief_of_staff)

#
# CTO Profile
#

chief_technology_officer = ExecutiveProfile(
    "AI Chief Technology Officer"
)

chief_technology_officer.add_skill(
    "validate_architecture"
)

chief_technology_officer.add_skill(
    "review_code"
)

chief_technology_officer.add_skill(
    "design_system"
)

register(chief_technology_officer)

__all__ = [
    "ExecutiveProfile",
    "ExecutiveManager",
    "executive_manager",
    "register",
    "get",
    "all",
]