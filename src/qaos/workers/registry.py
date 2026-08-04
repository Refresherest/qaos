"""
QAOS Worker Registry
"""

_WORKERS = {}


def register(worker):

    _WORKERS[
        worker.name
    ] = worker


def get(name):

    return _WORKERS.get(name)


def all():

    return dict(_WORKERS)