"""
QAOS Council Assignment
"""


class Assignment:

    def __init__(self, member, objective):

        self.member = member
        self.objective = objective

    def execute(self):

        print(
            f"[Council] {self.member.title}"
            f" accepted objective:"
        )

        print(f"    {self.objective.goal}")

        return self.member.run()