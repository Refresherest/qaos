"""
QAOS Knowledge Registry
"""

_registry = {}


def register(knowledge):

    _registry[knowledge.title] = knowledge


def get(title):

    return _registry.get(title)


def all():

    return _registry