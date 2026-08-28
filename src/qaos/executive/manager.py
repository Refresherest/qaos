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

    def __init__(self, orchestrator_service=None, logger_service=None):
        self._orchestrator = (
            orchestrator
            if orchestrator_service is None
            else orchestrator_service
        )
        self._logger = logger if logger_service is None else logger_service

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
