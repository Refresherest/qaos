"""
QAOS Task
"""

from datetime import datetime


class Task:

    def __init__(self, description):

        self.description = description

        # compatibility
        self.name = description

        self.status = "pending"

        self.started = None
        self.completed = None

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

        return {

            "description": self.description,

            "status": self.status,

            "started":
                self.started.isoformat()
                if self.started else None,

            "completed":
                self.completed.isoformat()
                if self.completed else None,

        }

    # ---------------------------------

    @classmethod
    def from_dict(cls, data):

        task = cls(
            data["description"]
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