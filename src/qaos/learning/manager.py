"""
QAOS Learning Manager
"""

from .learner import learner


class LearningManager:

    def learn(self, reflection):

        return learner.learn(
            reflection
        )


learning_manager = LearningManager()