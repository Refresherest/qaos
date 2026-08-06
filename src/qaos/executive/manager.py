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

    def execute(
        self,
        objective,
    ):

        logger.info(
            f"Executive executing '{objective.goal}'"
        )

        result = orchestrator.execute(
            objective
        )

        logger.info(
            "Executive execution complete."
        )

        return result


executive_manager = ExecutiveManager()