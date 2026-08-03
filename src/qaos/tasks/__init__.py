"""
QAOS Task System
"""

from .base import Task
from .manager import TaskManager

task_manager = TaskManager()

__all__ = [
    "Task",
    "TaskManager",
    "task_manager",
]