from .workflow import Workflow
from .manager import workflow_manager
from .registry import register, get, all

from .builtin import StartupWorkflow

register("startup", StartupWorkflow())

__all__ = [
    "Workflow",
    "workflow_manager",
    "register",
    "get",
    "all",
]