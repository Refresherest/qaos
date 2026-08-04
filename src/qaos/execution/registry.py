"""
QAOS Execution Registry
"""

ENGINES = {}


def register(name, engine):
    ENGINES[name] = engine


def get(name):
    return ENGINES.get(name)


def all():
    return ENGINES