"""
QAOS Capability Base
"""


class Capability:

    def __init__(
        self,
        name,
        description,
    ):
        self.name = name
        self.description = description

    def initialize(self):
        print(f"[Capability] Initializing {self.name}")

    def execute(self, *args, **kwargs):
        raise NotImplementedError

    def shutdown(self):
        print(f"[Capability] Shutting down {self.name}")