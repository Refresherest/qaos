"""
QAOS Executive Manager
"""

from qaos.logging import logger

from .orchestrator import (
    orchestrator,
)


class ExecutiveManager:
    """
    Public interface for the QAOS Executive.

    The Executive Manager is responsible for
    routing Objectives through the Executive
    Orchestrator.
    """

    def __init__(
        self, orchestrator_service=None, logger_service=None, *, recovery_service=None,
        intent_planner=None, intent_objectives=None,
    ):
        self._orchestrator = (
            orchestrator
            if orchestrator_service is None
            else orchestrator_service
        )
        self._logger = logger if logger_service is None else logger_service
        self._recovery = recovery_service
        self._intent_planner = intent_planner
        self._intent_objectives = intent_objectives

    def validate_intent(self, objective, intent):
        """Reject unsupported submission before pipeline writes."""
        if self._intent_planner is None or self._intent_objectives is None:
            raise RuntimeError("Executable intent submission is not enabled.")
        from qaos.objectives.objective import Objective

        if not isinstance(objective, Objective):
            raise TypeError("intent submission requires a canonical Objective")
        if (objective.objective_id is None
                or self._intent_objectives.get_by_id(objective.objective_id) is not objective):
            raise ValueError("Objective does not belong to this Executive")
        if objective.status != "pending":
            raise ValueError("intent submission requires a pending Objective")
        self._intent_planner.validate_intent_plan(objective, intent)

    def execute_intent(self, objective, intent):
        """Execute a call-specific intent through the existing pipeline."""
        self.validate_intent(objective, intent)
        self._logger.info(f"Executive executing '{objective.goal}'")
        result = self._orchestrator.execute(objective, intent=intent)
        self._logger.info("Executive execution complete.")
        return result

    def recover(self, objective_id):
        """Delegate explicitly configured recovery without running the pipeline."""
        if self._recovery is None:
            raise RuntimeError("No recovery service configured.")
        return self._recovery.recover(objective_id)

    def execute(
        self,
        objective,
    ):

        self._logger.info(
            f"Executive executing '{objective.goal}'"
        )

        result = self._orchestrator.execute(
            objective
        )

        self._logger.info(
            "Executive execution complete."
        )

        return result


executive_manager = ExecutiveManager()
