"""
QAOS Objective
"""

from datetime import datetime


class Objective:

    def __init__(self, goal):

        self.goal = goal

        self.status = "pending"

        self.plan = None

        #
        # Executive ownership
        #

        self.owner = None

        self.created = datetime.now().isoformat()

        self.started = None

        self.completed = None

    # ----------------------------------

    def assign(
        self,
        member,
    ):
        """
        Assign ownership of this objective
        to a Council member.
        """

        self.owner = member

        from qaos.objectives import objective_manager

        objective_manager._save()

    # ----------------------------------

    def assign_plan(self, plan):

        self.plan = plan

        from qaos.objectives import objective_manager

        objective_manager._save()

    # ----------------------------------

    def start(self):

        self.status = "running"

        self.started = datetime.now().isoformat()

        from qaos.objectives import objective_manager

        objective_manager._save()

    # ----------------------------------

    def complete(self):

        self.status = "completed"

        self.completed = datetime.now().isoformat()

        from qaos.objectives import objective_manager

        objective_manager._save()

    # ----------------------------------

    def fail(self):

        self.status = "failed"

        self.completed = datetime.now().isoformat()

        from qaos.objectives import objective_manager

        objective_manager._save()

    # ----------------------------------

    def __repr__(self):

        owner = None

        if self.owner is not None:

            owner = getattr(
                self.owner,
                "name",
                str(self.owner),
            )

        return (
            f"<Objective "
            f"{self.goal}"
            f" owner={owner}>"
        )