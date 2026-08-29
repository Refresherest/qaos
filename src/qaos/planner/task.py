"""
QAOS Task
"""

from datetime import datetime


class Task:

    def __init__(self, description, task_id=None):

        self.description = description

        self._task_id = None
        if task_id is not None:
            self._assign_identity(task_id)

        # compatibility
        self.name = description

        self.status = "pending"

        self.started = None
        self.completed = None

    @property
    def task_id(self):
        return self._task_id

    def _assign_identity(self, task_id):
        if not isinstance(task_id, str) or not task_id:
            raise ValueError("task_id must be a non-empty string")

        if self._task_id is not None and self._task_id != task_id:
            raise ValueError("task_id is immutable once assigned")

        self._task_id = task_id

    # ---------------------------------

    def start(self):

        self.status = "running"
        self.started = datetime.now()

    # ---------------------------------

    def complete(self):

        self.status = "completed"
        self.completed = datetime.now()

    # ---------------------------------

    def fail(self):

        self.status = "failed"
        self.completed = datetime.now()

    # ---------------------------------

    def to_dict(self):

        data = {

            "description": self.description,

            "status": self.status,

            "started":
                self.started.isoformat()
                if self.started else None,

            "completed":
                self.completed.isoformat()
                if self.completed else None,

        }

        if self.task_id is not None:
            data["task_id"] = self.task_id

        return data

    # ---------------------------------

    @classmethod
    def from_dict(cls, data):

        task = cls(
            data["description"],
            task_id=data.get("task_id"),
        )

        task.status = data.get(
            "status",
            "pending",
        )

        started = data.get("started")

        completed = data.get("completed")

        task.started = (
            datetime.fromisoformat(started)
            if started
            else None
        )

        task.completed = (
            datetime.fromisoformat(completed)
            if completed
            else None
        )

        return task

    # ---------------------------------

    def __repr__(self):

        return (
            f"<Task "
            f"{self.status}: "
            f"{self.description}>"
        )
