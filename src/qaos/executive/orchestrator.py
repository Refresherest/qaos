"""
QAOS Executive Orchestrator
"""

from .pipeline import executive_pipeline
from .result import ExecutionResult


class ExecutiveOrchestrator:
    """
    Top-level executive coordinator.

    Responsible for:
        • Creating the execution result
        • Invoking the executive pipeline
        • Handling failures
        • Returning the final result

    The actual work is performed by the ExecutivePipeline.
    """

    def __init__(self, pipeline=None):
        self._pipeline = executive_pipeline if pipeline is None else pipeline

    def execute(self, objective):

        result = ExecutionResult(
            objective
        )

        try:

            self._pipeline.execute(
                objective,
                result,
            )

            result.complete()

        except Exception as exc:

            result.fail(exc)

            raise

        return result


orchestrator = ExecutiveOrchestrator()
