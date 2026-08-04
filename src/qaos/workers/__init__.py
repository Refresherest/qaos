"""
QAOS Workers
"""

from .worker import Worker
from .manager import (
    WorkerManager,
    worker_manager,
)

from .registry import (
    register,
    get,
    all,
)

register(
    Worker(
        "default"
    )
)

__all__ = [
    "Worker",
    "WorkerManager",
    "worker_manager",
    "register",
    "get",
    "all",
]