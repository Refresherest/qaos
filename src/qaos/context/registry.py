"""
QAOS Context Registry
"""

_registry = {}


def register(context):

    _registry[context.objective.goal] = context


def unregister(goal):

    _registry.pop(goal, None)


def get(goal):

    return _registry.get(goal)


def all():

    return _registry