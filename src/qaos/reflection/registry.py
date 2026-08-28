"""
QAOS Reflection Registry
"""

def _objective_key(objective):
    if hasattr(objective, "goal"):
        return objective.goal

    return objective


class ReflectionRegistry:
    """Registry state owned by one reflection-manager lifecycle."""

    def __init__(self):
        self._registry = {}

    def register(self, reflection):
        self._registry[_objective_key(reflection.objective)] = reflection

    def unregister(self, objective):
        self._registry.pop(_objective_key(objective), None)

    def get(self, objective):
        return self._registry.get(_objective_key(objective))

    def all(self):
        return self._registry


reflection_registry = ReflectionRegistry()


def register(reflection):
    reflection_registry.register(reflection)


def unregister(objective):
    reflection_registry.unregister(objective)


def get(objective):
    return reflection_registry.get(objective)


def all():
    return reflection_registry.all()
