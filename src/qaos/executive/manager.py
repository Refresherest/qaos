"""
QAOS Executive Manager
"""

from qaos.classifier import classifier_manager

from .registry import get, all


class ExecutiveManager:

    def get(self, title):

        return get(title)

    def executives(self):

        return all()

    def find_by_skill(self, skill):

        for profile in all().values():

            if profile.has_skill(skill):

                return profile

        return None

    def resolve(self, objective):

        skill = classifier_manager.classify(
            objective
        )

        if skill is None:

            return None

        return self.find_by_skill(skill)


executive_manager = ExecutiveManager()