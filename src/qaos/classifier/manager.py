"""
QAOS Intent Classifier Manager
"""

from .registry import classifier


class ClassifierManager:

    def __init__(self, classifier_service=None):
        self._classifier = (
            classifier if classifier_service is None else classifier_service
        )

    def classify(self, objective):

        return self._classifier.classify(objective)


classifier_manager = ClassifierManager()
