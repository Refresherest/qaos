from .memory import memory
from .manager import memory_manager
from .registry import register, get, all

register("default", memory)

__all__ = [
    "memory",
    "memory_manager",
    "register",
    "get",
    "all",
]