"""
QAOS Executive Council
"""

from .chief_of_staff import ChiefOfStaff
from .manager import council_manager
from .registry import register, get, all

register(ChiefOfStaff())

__all__ = [
    "ChiefOfStaff",
    "council_manager",
    "register",
    "get",
    "all",
]