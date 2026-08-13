"""
QAOS Execution Report
"""

from datetime import datetime


class ExecutionReport:

    def __init__(self, objective):

        self.objective = objective

        self.started = datetime.now().isoformat()

        self.finished = None

        self.success = False

        self.worker = None

        self.plan = None

        self.tasks = []

        self.actions = []

        self.artifacts = []

        self.error = None

    # -------------------------------------

    def complete(self):

        self.finished = datetime.now().isoformat()

        self.success = True

    # -------------------------------------

    def fail(self, error):

        self.finished = datetime.now().isoformat()

        self.success = False

        self.error = str(error)

    # -------------------------------------

    @property
    def duration(self):

        if self.finished is None:

            return None

        start = datetime.fromisoformat(
            self.started
        )

        finish = datetime.fromisoformat(
            self.finished
        )

        return (
            finish - start
        ).total_seconds()

    # -------------------------------------

    def __repr__(self):

        return (
            f"<ExecutionReport "
            f"objective={self.objective.goal!r} "
            f"success={self.success}>"
        )
