"""
QAOS Planner Manager
"""

from .planner import Planner
from .generator import plan_generator


class PlannerManager:

    def create(self, goal):

        return Planner(goal)

    def plan(self, objective):

        plan = plan_generator.generate(objective)

        objective.attach(plan)

        return plan


planner_manager = PlannerManager()