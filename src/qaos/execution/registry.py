"""
QAOS Execution Registry
"""

class ExecutionRegistry:
    """Execution-engine state owned by one execution-manager lifecycle."""

    def __init__(self):
        self._engines = {}

    def register(self, name, engine):
        self._engines[name] = engine

    def get(self, name):
        return self._engines.get(name)

    def all(self):
        return self._engines


execution_registry = ExecutionRegistry()
ENGINES = execution_registry.all()


def register(name, engine):
    execution_registry.register(name, engine)


def get(name):
    return execution_registry.get(name)


def all():
    return execution_registry.all()
