"""
QAOS Objective Registry
"""

class ObjectiveRegistry:
    """Registry state owned by one objective-manager lifecycle."""

    def __init__(self):
        self._registry = {}

    def register(self, objective):
        if hasattr(objective, "goal"):
            key = objective.goal
        else:
            key = objective

        self._registry[key] = objective

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


objective_registry = ObjectiveRegistry()


def register(objective):
    objective_registry.register(objective)


def unregister(objective):
    objective_registry.unregister(objective)


def get(objective):
    return objective_registry.get(objective)


def all():
    return objective_registry.all()
