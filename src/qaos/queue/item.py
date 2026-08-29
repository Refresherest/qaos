"""
QAOS Queue Item
"""


class QueueItem:

    def __init__(
        self,
        objective,
        assignee,
        action=None,
        objective_id=None,
        task_id=None,
    ):
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

        if objective_id is not None and (
            not isinstance(objective_id, str) or not objective_id
        ):
            raise ValueError("objective_id must be a non-empty string or None")

        self.objective = objective
        self.objective_id = objective_id
        self.assignee = assignee

        if action is None:
            if task_id is not None:
                raise ValueError("task_id requires a QueueItem action")
        else:
            inherited_task_id = getattr(action, "task_id", None)
            if task_id is not None and task_id != inherited_task_id:
                raise ValueError("task_id does not match QueueItem action identity")
            if task_id is None:
                task_id = inherited_task_id

        if task_id is not None and (
            not isinstance(task_id, str) or not task_id
        ):
            raise ValueError("task_id must be a non-empty string or None")

        self.task_id = task_id

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
