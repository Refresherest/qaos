"""Application-facing operational lifecycle for one QAOS workspace."""

from qaos.config import Configuration, create_configuration
from qaos.executive import create_executive
from qaos.kernel.kernel import Kernel
from qaos.objectives.manager import ObjectiveManager
from qaos.storage import Stores


class OperationalSession:
    """Create and execute canonical Objectives in one explicit workspace."""

    def __init__(self, stores, *, configuration=None, logger=None):
        if not isinstance(stores, Stores):
            raise TypeError("stores must be a Stores instance")

        if configuration is not None and not isinstance(
            configuration,
            Configuration,
        ):
            raise TypeError("configuration must be a Configuration instance")

        self._objectives = ObjectiveManager(stores=stores)
        executive = create_executive(
            stores,
            objectives=self._objectives,
            logger=logger,
        )
        self._kernel = Kernel(
            configuration=(
                create_configuration(stores.data_dir)
                if configuration is None
                else configuration
            ),
            executive=executive,
        )

    def execute_goal(self, goal):
        """Create a canonical Objective for goal and execute it."""
        if not isinstance(goal, str):
            raise TypeError("goal must be a string")

        if not goal.strip():
            raise ValueError("goal must be a non-empty string")

        objective = self._objectives.create(goal.strip())

        try:
            return self._kernel.execute_objective(objective)
        except Exception:
            if objective.status == "pending":
                self._objectives.fail(objective)
            raise
