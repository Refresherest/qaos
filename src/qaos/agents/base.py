"""
QAOS Base Agent
"""


class Agent:

    def __init__(
        self,
        name,
        title,
        description,
    ):
        self.name = name
        self.title = title
        self.description = description

    def initialize(self):
        print(f"[Agent] Initializing {self.title}")

    def run(self):
        raise NotImplementedError

    def shutdown(self):
        print(f"[Agent] Shutting down {self.title}")