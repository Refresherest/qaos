"""
QAOS Council Delegator
"""

from qaos.council.assignment import Assignment
from qaos.council.registry import council_registry
from qaos.objectives import objective_manager


class Delegator:

    """
    Chooses who owns an objective.

    For now every objective is routed to the
    AI Chief Technology Officer.

    Later this becomes intelligent.
    """

    def __init__(self, registry=None, objectives=None):
        self._registry = council_registry if registry is None else registry
        self._objectives = (
            objective_manager if objectives is None else objectives
        )

    def assign(self, objective):

        council = self._registry.all()

        member = council.get(
            "chief_technology_officer"
        )

        if member is None:

            member = next(
                iter(council.values())
            )

        self._objectives.assign(objective, member)

        return Assignment(
            member,
            objective,
        )


delegator = Delegator()
