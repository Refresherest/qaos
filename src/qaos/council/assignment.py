"""
QAOS Council Assignment
"""


class Assignment:
    """
    Represents work assigned to a council member.

    An Assignment is purely descriptive.
    It does NOT execute work.
    """

    def __init__(self, member, objective):

        self.member = member
        self.objective = objective

        self.status = "assigned"

    def complete(self):
        self.status = "completed"

    def fail(self):
        self.status = "failed"

    def __repr__(self):
        return (
            f"<Assignment "
            f"{self.member.title}: "
            f"{self.objective}>"
        )