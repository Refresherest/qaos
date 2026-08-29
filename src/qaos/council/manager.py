"""
QAOS Executive Council Manager
"""

from .registry import council_registry
from .delegator import delegator

from qaos.queue import (
    QueueItem,
    queue_manager,
)


class CouncilManager:

    def __init__(self, registry=None, delegator_service=None, queue=None):
        self._registry = council_registry if registry is None else registry
        self._delegator = (
            delegator if delegator_service is None else delegator_service
        )
        self._queue = queue_manager if queue is None else queue

    def members(self):

        return self._registry.all()

    # -------------------------------------

    def execute(self, name):

        member = self._registry.get(name)

        if member is None:

            raise ValueError(
                f"Unknown council member: {name}"
            )

        member.run()

    # -------------------------------------

    def initialize(self):

        for member in self._registry.all().values():

            member.initialize()

    # -------------------------------------

    def shutdown(self):

        for member in self._registry.all().values():

            member.shutdown()

    # -------------------------------------

    def delegate(self, objective):
        """
        Delegate an Objective to the appropriate
        Executive Council member.
        """

        assignment = self._delegator.assign(
            objective
        )

        item = QueueItem(
            objective=objective,
            assignee=assignment.member.title,
        )

        self._queue.add(item)

        print(
            f"[Queue] Added objective for "
            f"{assignment.member.title}"
        )

        return assignment.member


council_manager = CouncilManager()
