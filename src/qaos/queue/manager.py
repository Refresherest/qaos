"""
QAOS Queue Manager
"""

from .registry import add, all, clear


class QueueManager:

    def add(self, item):
        add(item)

    def items(self):
        return all()

    def clear(self):
        clear()


queue_manager = QueueManager()