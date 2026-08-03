"""
QAOS Executive Council
"""

from .chief_of_staff import ChiefOfStaff
from .chief_technology_officer import ChiefTechnologyOfficer

from .manager import council_manager
from .registry import register, get, all

register(ChiefOfStaff())
register(ChiefTechnologyOfficer())

__all__ = [
    "ChiefOfStaff",
    "ChiefTechnologyOfficer",
    "council_manager",
    "register",
    "get",
    "all",
]