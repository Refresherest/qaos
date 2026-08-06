"""
QAOS Plan Registry
"""

_registry = {}


def register(plan):

    objective = plan.objective

    if hasattr(objective, "goal"):
        objective = objective.goal

    _registry[objective] = plan


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