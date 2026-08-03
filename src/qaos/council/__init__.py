"""
QAOS Executive Council
"""

from .chief_of_staff import ChiefOfStaff
from .registry import register, get, all

register(ChiefOfStaff())

__all__ = [
    "ChiefOfStaff",
    "register",
    "get",
    "all",
]