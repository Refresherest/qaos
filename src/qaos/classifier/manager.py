"""
QAOS Intent Classifier Manager
"""

from .registry import classifier


class ClassifierManager:

    def classify(self, objective):

        return classifier.classify(objective)


classifier_manager = ClassifierManager()