"""
QAOS Artifact Registry
"""

_registry = {}


def register(artifact):

    _registry[artifact.title] = artifact


def get(title):

    return _registry.get(title)


def all():

    return _registry