"""
QAOS Execution Manager
"""

from .registry import register, get, all
from .engine import ExecutionEngine


class ExecutionManager:

    def execute(self, objective):

        engine = get("default")

        if engine is None:
            raise RuntimeError(
                "No execution engine registered."
            )

        return engine.execute(objective)

    def engines(self):
        return all()


register(
    "default",
    ExecutionEngine(),
)

execution_manager = ExecutionManager()