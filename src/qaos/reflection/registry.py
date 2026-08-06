"""
QAOS Reflection Registry
"""

_registry = {}


def register(reflection):

    objective = reflection.objective

    if hasattr(objective, "goal"):
        objective = objective.goal

    _registry[objective] = reflection


def unregister(objective):

    if hasattr(objective, "goal"):
        objective = objective.goal

    _registry.pop(
        objective,
        None,
    )


def get(objective):

    if hasattr(objective, "goal"):
        objective = objective.goal

    return _registry.get(
        objective
    )


def all():

    return _registry