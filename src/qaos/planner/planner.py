"""
QAOS Planner
"""

from .plan import Plan
from .resolver import resolver


class Planner:

    def create(self, goal):

        return Plan(goal)

    def task(
        self,
        plan,
        task_name,
        action,
    ):

        executor = resolver.resolve(task_name)

        plan.add_task(
            task_name,
            executor,
            action,
        )