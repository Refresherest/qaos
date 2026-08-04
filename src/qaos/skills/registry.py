"""
QAOS Skill Registry
"""

_registry = {}


def register(skill):

    _registry[skill.name] = skill


def get(name):

    return _registry.get(name)


def all():

    return _registry