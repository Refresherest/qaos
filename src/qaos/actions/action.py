"""
QAOS Action
"""


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