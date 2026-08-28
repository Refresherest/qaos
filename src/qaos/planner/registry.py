"""
QAOS Plan Registry
"""

class PlanRegistry:
    """Registry state owned by one planner-manager lifecycle."""

    def __init__(self):
        self._registry = {}

    def register(self, plan):
        objective = plan.objective

        if hasattr(objective, "goal"):
            objective = objective.goal

        self._registry[objective] = plan

    def unregister(self, objective):
        if hasattr(objective, "goal"):
            objective = objective.goal

        self._registry.pop(objective, None)

    def get(self, objective):
        if hasattr(objective, "goal"):
            objective = objective.goal

        return self._registry.get(objective)

    def all(self):
        return self._registry


plan_registry = PlanRegistry()


def register(plan):
    plan_registry.register(plan)


def unregister(objective):
    plan_registry.unregister(objective)


def get(objective):
    return plan_registry.get(objective)


def all():
    return plan_registry.all()
