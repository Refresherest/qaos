"""
QAOS Executive Profile
"""


class ExecutiveProfile:

    def __init__(self, title):

        self.title = title
        self._skills = []

    def add_skill(self, skill):

        self._skills.append(skill)

    def remove_skill(self, skill):

        if skill in self._skills:
            self._skills.remove(skill)

    def has_skill(self, skill):

        return skill in self._skills

    def skills(self):

        return list(self._skills)

    def __repr__(self):

        return (
            f"<ExecutiveProfile "
            f"{self.title}: "
            f"{len(self._skills)} skills>"
        )