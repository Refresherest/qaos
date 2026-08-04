"""
QAOS Plan Task
"""


class Task:

    def __init__(
        self,
        name,
        executor,
        action,
    ):
        self.name = name
        self.executor = executor
        self.action = action

    def execute(self):

        print(f"[Task] {self.executor} -> {self.name}")

        return self.action()