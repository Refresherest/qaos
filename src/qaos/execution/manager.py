"""
QAOS Execution Manager
"""

from .registry import (
    register,
    get,
    all,
)

from .engine import ExecutionEngine

from qaos.objectives import objective_manager


class ExecutionManager:

    def execute(self, objective):

        engine = get("default")

        if engine is None:

            raise RuntimeError(
                "No execution engine registered."
            )

        #
        # Execute objective
        #

        report = engine.execute(
            objective
        )

        #
        # Persist objective state
        #

        objective_manager.save()

        return report

    # ---------------------------------

    def engines(self):

        return all()


#
# Register default execution engine
#

register(
    "default",
    ExecutionEngine(),
)

execution_manager = ExecutionManager()
