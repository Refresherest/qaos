class Workflow:
    """
    Base class for QAOS workflows.
    """

    name = "workflow"

    def execute(self):
        raise NotImplementedError