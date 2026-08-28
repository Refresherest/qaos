"""
QAOS Learner
"""

from .engine import learning_engine


class Learner:

    def __init__(self, engine=None):
        self._engine = learning_engine if engine is None else engine

    def learn(self, reflection):

        print(
            f"[Learner] Learning from "
            f"{reflection.objective.goal}"
        )

        return self._engine.learn(
            reflection
        )


learner = Learner()
