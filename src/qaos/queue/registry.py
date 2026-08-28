"""
QAOS Queue Registry
"""

class QueueRegistry:
    """Queue state owned by one queue-manager lifecycle."""

    def __init__(self):
        self._queue = []

    def add(self, item):
        self._queue.append(item)

    def all(self):
        return list(self._queue)

    def clear(self):
        self._queue.clear()


queue_registry = QueueRegistry()


def add(item):
    queue_registry.add(item)


def all():
    return queue_registry.all()


def clear():
    queue_registry.clear()
