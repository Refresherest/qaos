"""
QAOS Plan
"""

from .task import Task


class Plan:

    def __init__(self, objective, objective_id=None):

        if hasattr(objective, "goal"):
            inherited_id = getattr(objective, "objective_id", None)
            if (
                objective_id is not None
                and inherited_id is not None
                and objective_id != inherited_id
            ):
                raise ValueError("objective_id does not match Objective identity")
            if objective_id is None:
                objective_id = inherited_id
            objective = objective.goal

        self.objective = objective
        self.objective_id = self._validate_objective_id(objective_id)

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

        data = {

            "objective": self.objective,

            "tasks": [
                task.to_dict()
                for task in self.tasks
            ],

        }

        if self.objective_id is not None:
            data["objective_id"] = self.objective_id

        return data

    # ---------------------------------

    @classmethod
    def from_dict(cls, data):

        plan = cls(
            data["objective"],
            objective_id=data.get("objective_id"),
        )

        for task_data in data.get(
            "tasks",
            [],
        ):

            plan.tasks.append(
                Task.from_dict(task_data)
            )

        return plan

    # ---------------------------------

    @staticmethod
    def _validate_objective_id(objective_id):
        if objective_id is not None and (
            not isinstance(objective_id, str) or not objective_id
        ):
            raise ValueError("objective_id must be a non-empty string or None")

        return objective_id

    # ---------------------------------

    def __repr__(self):

        return (
            f"<Plan "
            f"{self.objective} "
            f"tasks={len(self.tasks)}>"
        )
