"""
QAOS Memory Registry
"""

_registry = {}


def register(memory):

    _registry[memory.title] = memory


def unregister(title):

    if hasattr(title, "title"):
        title = title.title

    _registry.pop(title, None)


def get(title):

    if hasattr(title, "title"):
        title = title.title

    return _registry.get(title)


def all():

    return _registry