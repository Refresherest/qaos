"""
QAOS Objective Manager
"""

from .objective import Objective
from .registry import register, all, clear


class ObjectiveManager:

    def create(self, goal):

        objective = Objective(goal)

        register(objective)

        return objective

    def objectives(self):
        return all()

    def clear(self):
        clear()


objective_manager = ObjectiveManager()