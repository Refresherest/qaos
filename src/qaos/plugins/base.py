"""
QAOS Plugin Base Class
"""


class Plugin:

    def __init__(
        self,
        name,
        version="0.1.0",
        description="",
    ):
        self.name = name
        self.version = version
        self.description = description

    def initialize(self):
        print(f"[Plugin] Initializing {self.name}")

    def shutdown(self):
        print(f"[Plugin] Shutting down {self.name}")

    def execute(self):
        pass