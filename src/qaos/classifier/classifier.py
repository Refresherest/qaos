"""
QAOS Intent Classifier
"""


class IntentClassifier:

    def __init__(self):

        self._rules = {}

    def register(self, keyword, skill):

        self._rules[keyword.lower()] = skill

    def classify(self, objective):

        text = objective.lower()

        for keyword, skill in self._rules.items():

            if keyword in text:

                return skill

        return None

    def __repr__(self):

        return (
            f"<IntentClassifier "
            f"{len(self._rules)} rules>"
        )