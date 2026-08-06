"""
QAOS Executive Council Manager
"""

from .registry import get, all
from .delegator import delegator

from qaos.queue import (
    QueueItem,
    queue_manager,
)


class CouncilManager:

    def members(self):

        return all()

    # -------------------------------------

    def execute(self, name):

        member = get(name)

        if member is None:

            raise ValueError(
                f"Unknown council member: {name}"
            )

        member.run()

    # -------------------------------------

    def initialize(self):

        for member in all().values():

            member.initialize()

    # -------------------------------------

    def shutdown(self):

        for member in all().values():

            member.shutdown()

    # -------------------------------------

    def delegate(self, objective):
        """
        Delegate an Objective to the appropriate
        Executive Council member.
        """

        assignment = delegator.assign(
            objective
        )

        item = QueueItem(
            objective=objective.goal,
            assignee=assignment.member.title,
        )

        queue_manager.add(item)

        print(
            f"[Queue] Added objective for "
            f"{assignment.member.title}"
        )

        return assignment.member


council_manager = CouncilManager()