"""
QAOS Task Base Class
"""


class Task:
    """
    Base class for all QAOS tasks.
    """

    name = "task"

    def execute(self):
        raise NotImplementedError("Tasks must implement execute().")