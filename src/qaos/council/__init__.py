"""
QAOS Executive Council
"""

from .chief_of_staff import ChiefOfStaff
from .chief_technology_officer import ChiefTechnologyOfficer

from .objective import Objective
from .assignment import Assignment
from .delegator import delegator

from .manager import (
    CouncilManager,
    council_manager,
)

# Register built-in council members
ChiefOfStaff()
ChiefTechnologyOfficer()

# Register lifecycle events
from . import lifecycle

__all__ = [
    "ChiefOfStaff",
    "ChiefTechnologyOfficer",
    "Objective",
    "Assignment",
    "delegator",
    "CouncilManager",
    "council_manager",
]