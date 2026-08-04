"""
QAOS Queue Manager
"""

from .registry import (
    add,
    all,
)

from qaos.workers import worker_manager


class QueueManager:

    def add(self, item):
        add(item)

    def items(self):
        return all()

    def process(self):
        """
        Process every pending queue item.
        """

        worker = worker_manager.get(
            "default"
        )

        for item in all():

            if item.status != "pending":
                continue

            worker.execute(item)


queue_manager = QueueManager()