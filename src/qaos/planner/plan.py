"""
QAOS Execution Plan
"""

from .task import Task


class Plan:

    def __init__(self, goal):

        self.goal = goal
        self.tasks = []

    def add_task(
        self,
        name,
        executor,
        action,
    ):

        self.tasks.append(

            Task(
                name,
                executor,
                action,
            )

        )

    def execute(self):

        results = []

        for task in self.tasks:

            results.append(
                task.execute()
            )

        return results