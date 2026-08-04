"""
QAOS Queue Item
"""


class QueueItem:

    def __init__(
        self,
        objective,
        assignee,
        action=None,
    ):
        self.objective = objective
        self.assignee = assignee

        self.action = action

        self.status = "pending"

        self.result = None

        self.started = None
        self.completed = None

    def __repr__(self):
        return (
            f"<QueueItem "
            f"objective={self.objective!r} "
            f"assignee={self.assignee!r} "
            f"status={self.status!r}>"
        )