"""
QAOS Objective Registry
"""

_registry = {}


def register(objective):

    if hasattr(objective, "goal"):
        key = objective.goal
    else:
        key = objective

    _registry[key] = objective


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