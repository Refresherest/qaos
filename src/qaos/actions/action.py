"""
QAOS Action
"""

from qaos.capabilities import capability_manager


class Action:
    """
    Represents one executable action.
    """

    def __init__(
        self,
        name,
        capability,
        operation,
        *args,
        priority="normal",
        creator=None,
        description="",
        artifact=None,
        **kwargs,
    ):

        self.name = name
        self.capability = capability
        self.operation = operation

        self.args = args
        self.kwargs = kwargs

        self.priority = priority
        self.creator = creator
        self.description = description

        self.artifact = artifact

    def execute(self):
        """
        Executes the action through its capability.
        """

        capability = capability_manager.get(
            self.capability
        )

        if capability is None:

            raise RuntimeError(
                f"Capability '{self.capability}' not found."
            )

        print(
            f"[Action] {self.name}"
        )

        result = capability.execute(
            self.operation,
            *self.args,
            **self.kwargs,
        )

        if self.artifact is not None:

            return self.artifact(result)

        return result

    def info(self):

        return {
            "name": self.name,
            "capability": self.capability,
            "operation": self.operation,
            "priority": self.priority,
            "creator": self.creator,
            "description": self.description,
        }

    def __repr__(self):

        return (
            f"<Action "
            f"{self.name} "
            f"[{self.priority}]>"
        )