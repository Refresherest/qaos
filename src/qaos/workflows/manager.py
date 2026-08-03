from qaos.workflows.registry import get


class WorkflowManager:

    def execute(self, name):
        workflow = get(name)

        if workflow is None:
            raise ValueError(f"Unknown workflow: {name}")

        return workflow.execute()


workflow_manager = WorkflowManager()