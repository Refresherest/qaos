"""
QAOS Council
"""

from .registry import register

from .manager import (
    CouncilManager,
    council_manager,
)

from .router import (
    CouncilRouter,
    council_router,
)

from .delegator import Delegator
from .assignment import Assignment

from .chief_of_staff import ChiefOfStaff
from .chief_technology_officer import (
    ChiefTechnologyOfficer,
)

# -------------------------------------------------
# Register Executive Council Members
# -------------------------------------------------

register(
    ChiefOfStaff()
)

register(
    ChiefTechnologyOfficer()
)

__all__ = [

    "CouncilManager",
    "council_manager",

    "CouncilRouter",
    "council_router",

    "Delegator",
    "Assignment",

    "ChiefOfStaff",
    "ChiefTechnologyOfficer",

]