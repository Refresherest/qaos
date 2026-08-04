"""
QAOS Workflow Base Class
"""


class Workflow:

    def __init__(
        self,
        name,
        description,
    ):
        self.name = name
        self.description = description

    def initialize(self):
        print(f"[Workflow] Initializing {self.name}")

    def execute(self):
        raise NotImplementedError

    def shutdown(self):
        print(f"[Workflow] Shutting down {self.name}")