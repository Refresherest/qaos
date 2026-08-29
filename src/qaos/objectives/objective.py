"""
QAOS Objective
"""

from datetime import datetime


class Objective:

    def __init__(self, goal, objective_id=None):

        self.goal = goal

        self._objective_id = None
        if objective_id is not None:
            self._assign_identity(objective_id)

        self.status = "pending"

        self.plan = None

        #
        # Executive ownership
        #

        self.owner = None

        self.created = datetime.now().isoformat()

        self.started = None

        self.completed = None

    @property
    def objective_id(self):
        return self._objective_id

    def _assign_identity(self, objective_id):
        if not isinstance(objective_id, str) or not objective_id:
            raise ValueError("objective_id must be a non-empty string")

        if self._objective_id is not None and self._objective_id != objective_id:
            raise ValueError("objective_id is immutable once assigned")

        self._objective_id = objective_id

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

    # ----------------------------------

    def assign_plan(self, plan):

        self.plan = plan

    # ----------------------------------

    def start(self):

        self.status = "running"

        self.started = datetime.now().isoformat()

    # ----------------------------------

    def complete(self):

        self.status = "completed"

        self.completed = datetime.now().isoformat()

    # ----------------------------------

    def fail(self):

        self.status = "failed"

        self.completed = datetime.now().isoformat()

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
