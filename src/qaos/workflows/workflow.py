"""
QAOS Workflow Base Class
"""

from qaos.actions import Action


class Workflow:

    def __init__(
        self,
        name,
        description="",
    ):
        self.name = name
        self.description = description

        self.actions = []

        self.status = "pending"

        self.started = None
        self.completed = None

    def initialize(self):
        print(
            f"[Workflow] Initializing {self.name}"
        )

    def add(self, action):

        if not isinstance(action, Action):

            raise TypeError(
                "Workflow only accepts Action objects."
            )

        self.actions.append(action)

    def remove(self, action):

        self.actions.remove(action)

    def clear(self):

        self.actions.clear()

    def execute(self):
        """
        Override in subclasses if desired.
        """
        raise NotImplementedError

    def shutdown(self):
        print(
            f"[Workflow] Shutting down {self.name}"
        )

    def __iter__(self):

        return iter(self.actions)

    def __len__(self):

        return len(self.actions)

    def info(self):

        return {
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "actions": [
                action.info()
                for action in self.actions
            ],
        }

    def __repr__(self):

        return (
            f"<Workflow "
            f"{self.name} "
            f"({len(self.actions)} actions)>"
        )