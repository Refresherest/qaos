"""
QAOS Executive Council
"""

from .chief_of_staff import ChiefOfStaff
from .chief_technology_officer import ChiefTechnologyOfficer

from .registry import register
from .manager import CouncilManager, council_manager

# ------------------------------------------------------------------
# Register built-in Executive Council members
# ------------------------------------------------------------------

register(ChiefOfStaff())
register(ChiefTechnologyOfficer())

# Import lifecycle AFTER registration so subscriptions are installed.
from . import lifecycle

__all__ = [
    "ChiefOfStaff",
    "ChiefTechnologyOfficer",
    "CouncilManager",
    "council_manager",
]