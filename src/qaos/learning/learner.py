"""
QAOS Learner
"""

from .engine import learning_engine


class Learner:

    def __init__(self, engine=None):
        self._engine = learning_engine if engine is None else engine

    def learn(self, reflection):

        objective = reflection.objective
        goal = objective.goal if hasattr(objective, "goal") else objective

        print(
            f"[Learner] Learning from "
            f"{goal}"
        )

        return self._engine.learn(
            reflection
        )


learner = Learner()
