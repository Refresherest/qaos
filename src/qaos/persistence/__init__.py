"""
QAOS Persistence Package
"""

from .database import Database
from .json_store import JSONStore

from .registry import register
from .registry import get
from .registry import all

from .manager import (
    PersistenceManager,
    persistence_manager,
)

register(
    "json",
    JSONStore()
)

__all__ = [
    "Database",
    "JSONStore",
    "PersistenceManager",
    "persistence_manager",
    "register",
    "get",
    "all",
]