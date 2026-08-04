"""
QAOS Planner Manager
"""

from .planner import Planner


class PlannerManager:

    def __init__(self):
        self.planner = Planner()

    def create(self, goal):
        return self.planner.create(goal)

    def task(
        self,
        plan,
        task_name,
        action,
    ):
        return self.planner.task(
            plan,
            task_name,
            action,
        )


planner_manager = PlannerManager()