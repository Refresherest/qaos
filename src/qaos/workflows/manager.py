"""
QAOS Workflow Manager
"""

from qaos.workflows.registry import (
    register,
    unregister,
    get,
    all_workflows,
)


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

    def execute(self, name):
        workflow = get(name)

        if workflow is None:
            raise ValueError(
                f"Unknown workflow: {name}"
            )

        return workflow.execute()


workflow_manager = WorkflowManager()