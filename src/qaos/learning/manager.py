"""
QAOS Learning Manager
"""

from .learner import learner


class LearningManager:

    def __init__(self, learner_service=None):
        self._learner = learner if learner_service is None else learner_service

    def learn(self, reflection):

        return self._learner.learn(
            reflection
        )


learning_manager = LearningManager()
