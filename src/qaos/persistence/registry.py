"""
QAOS Persistence Registry
"""

BACKENDS = {}


def register(name, backend):
    BACKENDS[name] = backend


def get(name):
    return BACKENDS.get(name)


def all():
    return BACKENDS