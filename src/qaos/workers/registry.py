"""
QAOS Worker Registry
"""

class WorkerRegistry:
    """Registry state owned by one worker-manager lifecycle."""

    def __init__(self):
        self._workers = {}

    def register(self, worker):
        self._workers[worker.name] = worker

    def unregister(self, name):
        self._workers.pop(name, None)

    def get(self, name):
        return self._workers.get(name)

    def all(self):
        return dict(self._workers)

    def clear(self):
        self._workers.clear()


worker_registry = WorkerRegistry()


def register(worker):
    """
    Register a worker.
    """

    worker_registry.register(worker)


def unregister(name):
    """
    Remove a worker.
    """

    worker_registry.unregister(name)


def get(name):
    """
    Return a worker by name.
    """

    return worker_registry.get(name)


def all():
    """
    Return all registered workers.
    """

    return worker_registry.all()


def clear():
    """
    Remove every worker.
    """

    worker_registry.clear()
