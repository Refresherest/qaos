"""
QAOS Persistence Registry
"""

PERSISTENCE = {}


def register(store):
    PERSISTENCE[store.name] = store


def unregister(name):
    PERSISTENCE.pop(name, None)


def get(name):
    return PERSISTENCE.get(name)


def all_stores():
    return PERSISTENCE