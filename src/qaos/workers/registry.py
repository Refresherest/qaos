"""
QAOS Worker Registry
"""

_WORKERS = {}


def register(worker):
    """
    Register a worker.
    """

    _WORKERS[worker.name] = worker


def unregister(name):
    """
    Remove a worker.
    """

    _WORKERS.pop(name, None)


def get(name):
    """
    Return a worker by name.
    """

    return _WORKERS.get(name)


def all():
    """
    Return all registered workers.
    """

    return dict(_WORKERS)


def clear():
    """
    Remove every worker.
    """

    _WORKERS.clear()