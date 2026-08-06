"""
QAOS Workflow Framework
"""

from .workflow import Workflow

from .manager import (
    WorkflowManager,
    workflow_manager,
)

from .registry import (
    register,
    unregister,
    get,
    all_workflows,
)

from .executor import (
    WorkflowExecutor,
    workflow_executor,
)

from .builtin import StartupWorkflow

workflow_manager.register(
    StartupWorkflow()
)

__all__ = [

    "Workflow",

    "WorkflowManager",
    "workflow_manager",

    "WorkflowExecutor",
    "workflow_executor",

    "register",
    "unregister",
    "get",
    "all_workflows",

]