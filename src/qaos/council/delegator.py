"""
QAOS Council Delegator
"""

from qaos.council.assignment import Assignment
from qaos.council.registry import all
from qaos.objectives import objective_manager


class Delegator:

    """
    Chooses who owns an objective.

    For now every objective is routed to the
    AI Chief Technology Officer.

    Later this becomes intelligent.
    """

    def assign(self, objective):

        council = all()

        member = council.get(
            "chief_technology_officer"
        )

        if member is None:

            member = next(
                iter(council.values())
            )

        objective_manager.assign(objective, member)

        return Assignment(
            member,
            objective,
        )


delegator = Delegator()
