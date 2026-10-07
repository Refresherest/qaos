"""
QAOS Queue Item
"""

from copy import deepcopy


class QueueItem:

    def __init__(
        self,
        objective,
        assignee,
        action=None,
        objective_id=None,
        task_id=None,
        queue_item_id=None,
        pilot_attempt=None,
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

        self._queue_item_id = None
        if queue_item_id is not None:
            self._assign_identity(queue_item_id)

        self._pilot_attempt = None
        if pilot_attempt is not None:
            self._assign_pilot_attempt(pilot_attempt)

        self.action = action

        self.status = "pending"

        self.result = None

        self.started = None
        self.completed = None

    @property
    def queue_item_id(self):
        return self._queue_item_id

    def _assign_identity(self, queue_item_id):
        if not isinstance(queue_item_id, str) or not queue_item_id:
            raise ValueError("queue_item_id must be a non-empty string")
        if self._queue_item_id is not None and self._queue_item_id != queue_item_id:
            raise ValueError("queue_item_id is immutable once assigned")
        self._queue_item_id = queue_item_id

    @property
    def pilot_attempt(self):
        return deepcopy(self._pilot_attempt)

    def _assign_pilot_attempt(self, pilot_attempt):
        if not isinstance(pilot_attempt, dict) or not pilot_attempt:
            raise ValueError("pilot_attempt must be a non-empty dict")
        if self._pilot_attempt is not None and self._pilot_attempt != pilot_attempt:
            raise ValueError("pilot_attempt is immutable once assigned")
        self._pilot_attempt = deepcopy(pilot_attempt)

    def __repr__(self):
        return (
            f"<QueueItem "
            f"objective={self.objective!r} "
            f"assignee={self.assignee!r} "
            f"status={self.status!r}>"
        )
