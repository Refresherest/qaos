"""
QAOS Worker Manager
"""

from .registry import (
    register,
    unregister,
    get,
    all,
)

from .default import default_worker


class WorkerManager:

    def __init__(self):

        #
        # Register the default worker
        # once when QAOS starts.
        #

        if get(default_worker.name) is None:

            register(default_worker)

    # ---------------------------------

    def register(self, worker):

        register(worker)

    # ---------------------------------

    def unregister(self, name):

        unregister(name)

    # ---------------------------------

    def get(self, name="default"):

        return get(name)

    # ---------------------------------

    def workers(self):

        return all()

    # ---------------------------------

    def execute(self, item):

        worker = self.get()

        if worker is None:

            raise RuntimeError(
                "No worker registered."
            )

        return worker.execute(item)


worker_manager = WorkerManager()