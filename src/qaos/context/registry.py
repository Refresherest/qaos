"""
QAOS Context Registry
"""

class ContextRegistry:
    """Registry state owned by one context-manager lifecycle."""

    def __init__(self):
        self._registry = {}

    def register(self, context):
        self._registry[context.objective.goal] = context

    def unregister(self, goal):
        self._registry.pop(goal, None)

    def get(self, goal):
        return self._registry.get(goal)

    def all(self):
        return self._registry


context_registry = ContextRegistry()


def register(context):
    context_registry.register(context)


def unregister(goal):
    context_registry.unregister(goal)


def get(goal):
    return context_registry.get(goal)


def all():
    return context_registry.all()
