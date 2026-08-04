"""
QAOS Executive Briefing
"""


class Briefing:

    def __init__(self, objective):

        self.objective = objective
        self.notes = []

    def add(self, author, note):

        self.notes.append(
            {
                "author": author,
                "note": note,
            }
        )