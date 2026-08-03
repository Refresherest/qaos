"""
QAOS Memory Registry
"""

MEMORIES = {}


def register(name, store):
    MEMORIES[name] = store


def get(name):
    return MEMORIES.get(name)


def all():
    return MEMORIES