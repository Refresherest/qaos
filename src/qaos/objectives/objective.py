"""
QAOS Objective
"""


class Objective:

    def __init__(self, goal: str):

        self.goal = goal
        self.status = "pending"

        self.owner = None
        self.plan = None

    def assign(self, owner):
        self.owner = owner

    def attach(self, plan):
        self.plan = plan

    def start(self):
        self.status = "running"

    def complete(self):
        self.status = "completed"

    def fail(self):
        self.status = "failed"

    def __repr__(self):
        return (
            f"Objective("
            f"goal={self.goal!r}, "
            f"status={self.status!r}"
            f")"
        )