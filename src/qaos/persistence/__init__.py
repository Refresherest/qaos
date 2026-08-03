"""
QAOS Persistence Package
"""

from .database import Database
from .json_store import JSONStore

from .sqlite_store import SQLiteStore

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

register(
    "sqlite",
    SQLiteStore()
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