"""
QAOS Execution Manager
"""

from .registry import (
    register,
    get,
    all,
)

from .engine import ExecutionEngine

from qaos.reflection import reflection_manager
from qaos.learning import learning_manager
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

        #
        # Learn from the Reflection,
        # not the ExecutionReport.
        #

        reflection = reflection_manager.get(
            objective
        )

        if reflection is not None:

            learning_manager.learn(
                reflection
            )

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