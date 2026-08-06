"""
QAOS Workflow Executor
"""

from datetime import datetime

from qaos.actions import action_manager
from qaos.logging import logger


class WorkflowExecutor:

    def execute(self, workflow):

        logger.info(
            f"Executing workflow '{workflow.name}'"
        )

        workflow.status = "running"
        workflow.started = datetime.now()

        results = []

        try:

            for action in workflow:

                result = action_manager.execute(
                    action
                )

                results.append(result)

            workflow.status = "completed"

        except Exception:

            workflow.status = "failed"
            raise

        finally:

            workflow.completed = datetime.now()

        logger.info(
            f"Completed workflow '{workflow.name}'"
        )

        return results


workflow_executor = WorkflowExecutor()