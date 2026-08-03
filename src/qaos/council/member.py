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
        """
        Executed when the Executive Council starts.
        """
        pass

    def shutdown(self):
        """
        Executed when QAOS shuts down.
        """
        pass