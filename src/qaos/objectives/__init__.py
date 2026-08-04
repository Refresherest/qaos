"""
QAOS Objectives
"""

from .objective import Objective
from .manager import (
    ObjectiveManager,
    objective_manager,
)

__all__ = [
    "Objective",
    "ObjectiveManager",
    "objective_manager",
]