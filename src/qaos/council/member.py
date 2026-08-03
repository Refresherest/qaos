"""
QAOS Executive Council Member
"""

from qaos.agents.base import Agent


class CouncilMember(Agent):

    def __init__(
        self,
        name,
        title,
        description,
    ):
        super().__init__(
            name=name,
            title=title,
            description=description,
        )

    def initialize(self):
        print(f"[Council] Initializing {self.title}")

    def run(self):
        raise NotImplementedError

    def shutdown(self):
        print(f"[Council] Shutting down {self.title}")