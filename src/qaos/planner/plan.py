"""
QAOS Plan
"""

from .task import Task


class Plan:

    def __init__(self, objective):

        if hasattr(objective, "goal"):
            objective = objective.goal

        self.objective = objective

        self.tasks = []

    # ---------------------------------

    def add_task(self, task):

        if isinstance(task, str):
            task = Task(task)

        self.tasks.append(task)

        return task

    # ---------------------------------

    def remove_task(self, task):

        self.tasks.remove(task)

    # ---------------------------------

    def clear(self):

        self.tasks.clear()

    # ---------------------------------

    def completed(self):

        return all(
            task.status == "completed"
            for task in self.tasks
        )

    # ---------------------------------

    def to_dict(self):

        return {

            "objective": self.objective,

            "tasks": [
                task.to_dict()
                for task in self.tasks
            ],

        }

    # ---------------------------------

    @classmethod
    def from_dict(cls, data):

        plan = cls(data["objective"])

        for task_data in data.get(
            "tasks",
            [],
        ):

            plan.tasks.append(
                Task.from_dict(task_data)
            )

        return plan

    # ---------------------------------

    def __repr__(self):

        return (
            f"<Plan "
            f"{self.objective} "
            f"tasks={len(self.tasks)}>"
        )