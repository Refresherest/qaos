"""
QAOS Queue Item
"""


class QueueItem:

    def __init__(
        self,
        objective,
        assignee,
        priority="normal",
    ):
        self.objective = objective
        self.assignee = assignee
        self.priority = priority
        self.status = "pending"

    def start(self):
        self.status = "running"

    def complete(self):
        self.status = "completed"

    def fail(self):
        self.status = "failed"