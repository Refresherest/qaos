"""
QAOS Executive Execution Result
"""


class ExecutionResult:
    """
    Represents the complete result of an Executive execution.
    """

    def __init__(self, objective):

        self.objective = objective

        self.classification = None

        self.member = None

        self.plan = None

        self.workflow = None

        self.skill = None

        self.actions = []

        self.artifacts = []

        self.reflection = None

        self.success = False

        self.error = None

    @property
    def completed(self):

        return self.success

    def fail(self, error):

        self.success = False

        self.error = str(error)

    def complete(self):

        self.success = True

    def __repr__(self):

        return (
            f"<ExecutionResult "
            f"objective={self.objective!r} "
            f"success={self.success}>"
        )