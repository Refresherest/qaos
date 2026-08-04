"""
QAOS Executive Council Manager
"""

from .registry import get, all
from .objective import Objective
from .delegator import delegator


class CouncilManager:

    def members(self):

        return all()

    def execute(self, name):

        member = get(name)

        if member is None:

            raise ValueError(
                f"Unknown council member: {name}"
            )

        member.run()

    def initialize(self):

        for member in all().values():

            member.initialize()

    def shutdown(self):

        for member in all().values():

            member.shutdown()

    def objective(self, goal):

        return Objective(goal)

    def delegate(self, goal):

        objective = Objective(goal)

        assignment = delegator.assign(
            objective
        )

        assignment.execute()

        return objective


council_manager = CouncilManager()