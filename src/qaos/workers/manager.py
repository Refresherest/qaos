"""
QAOS Worker Manager
"""

from .registry import get, all


class WorkerManager:

    def get(self, name):
        return get(name)

    def workers(self):
        return all()

    def execute(self, item):

        worker = self.get("default")

        if worker is None:
            raise RuntimeError(
                "No default worker registered."
            )

        return worker.execute(item)


worker_manager = WorkerManager()