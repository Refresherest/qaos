"""Application-facing operational lifecycle for one QAOS workspace."""

from qaos.config import Configuration, create_configuration
from qaos.executive import create_executive
from qaos.kernel.kernel import Kernel
from qaos.objectives.manager import ObjectiveManager
from qaos.objectives.objective import Objective
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
        self._executive = executive
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
        return self.execute_objective(self.create_objective(goal))

    def create_objective(self, goal):
        """Create and persist one identified Objective in this workspace."""
        if not isinstance(goal, str):
            raise TypeError("goal must be a string")

        if not goal.strip():
            raise ValueError("goal must be a non-empty string")

        return self._objectives.create(goal.strip())

    def execute_objective(self, objective):
        """Execute only the canonical Objective registered in this session."""
        if not isinstance(objective, Objective):
            raise TypeError("objective must be a canonical QAOS Objective")
        if (objective.objective_id is None
                or self._objectives.get_by_id(objective.objective_id) is not objective):
            raise ValueError("objective must belong to this session")

        try:
            return self._kernel.execute_objective(objective)
        except Exception:
            if objective.status == "pending":
                self._objectives.fail(objective)
            raise

    def recover_objective(self, objective_id):
        """Recover an existing identified attempt in this session's workspace."""
        if not isinstance(objective_id, str):
            raise TypeError("objective_id must be a string")
        if not objective_id.strip():
            raise ValueError("objective_id must be a non-empty string")

        self._executive.recover(objective_id)
        return self._objectives.get_by_id(objective_id)
