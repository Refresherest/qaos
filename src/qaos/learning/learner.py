"""
QAOS Learner
"""

from .engine import learning_engine


class Learner:

    def learn(self, reflection):

        print(
            f"[Learner] Learning from "
            f"{reflection.objective.goal}"
        )

        return learning_engine.learn(
            reflection
        )


learner = Learner()