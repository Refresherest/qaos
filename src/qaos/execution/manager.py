"""
QAOS Execution Manager
"""

from .registry import execution_registry

from .engine import ExecutionEngine

from qaos.objectives import objective_manager


class ExecutionManager:

    def __init__(self, *, registry=None, objectives=None):
        self._registry = execution_registry if registry is None else registry
        self._objectives = objective_manager if objectives is None else objectives

    def execute(self, objective):

        engine = self._registry.get("default")

        if engine is None:

            raise RuntimeError(
                "No execution engine registered."
            )

        #
        # Execute objective
        #

        self._objectives.start(objective)

        try:
            report = engine.execute(
                objective
            )
        except Exception:
            self._objectives.fail(objective)
            raise

        self._objectives.complete(objective)

        return report

    # ---------------------------------

    def recover(self, objective_id):

        if not isinstance(objective_id, str) or not objective_id:
            raise ValueError("objective_id must be a non-empty string")

        engine = self._registry.get("default")
        if engine is None:
            raise RuntimeError("No execution engine registered.")

        objective = self._objectives.get_by_id(objective_id)
        if objective is None:
            raise ValueError("Objective not found for recovery")
        if objective.status != "failed":
            raise ValueError("only a failed Objective can be recovered")

        engine.validate_recovery(objective)
        self._objectives.start(objective)

        try:
            result = engine.recover(objective)
        except Exception:
            try:
                self._objectives.fail(objective)
            except Exception:
                pass
            raise

        self._objectives.complete(objective)
        return result

    # ---------------------------------

    def engines(self):

        return self._registry.all()


#
# Register default execution engine
#

execution_registry.register(
    "default",
    ExecutionEngine(),
)

execution_manager = ExecutionManager()
