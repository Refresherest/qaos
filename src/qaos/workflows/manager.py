"""
QAOS Workflow Manager
"""

from .registry import (
    register,
    unregister,
    get,
    all_workflows,
)

from .executor import workflow_executor


class WorkflowManager:

    def register(self, workflow):

        register(workflow)

    def unregister(self, name):

        unregister(name)

    def get(self, name):

        return get(name)

    def workflows(self):

        return all_workflows()

    def initialize(self):

        for workflow in all_workflows().values():

            workflow.initialize()

    def shutdown(self):

        for workflow in all_workflows().values():

            workflow.shutdown()

    def execute(self, workflow):

        if isinstance(workflow, str):

            workflow = get(workflow)

        if workflow is None:

            raise ValueError(
                "Unknown workflow."
            )

        return workflow_executor.execute(
            workflow
        )


workflow_manager = WorkflowManager()