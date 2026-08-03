from .database import Database
from .json_store import JSONStore

from .registry import register
from .registry import get
from .registry import all

register(
    "json",
    JSONStore()
)

__all__ = [
    "Database",
    "JSONStore",
    "register",
    "get",
    "all",
]