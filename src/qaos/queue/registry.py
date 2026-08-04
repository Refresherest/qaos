"""
QAOS Queue Registry
"""

_QUEUE = []


def add(item):
    _QUEUE.append(item)


def all():
    return list(_QUEUE)


def clear():
    _QUEUE.clear()