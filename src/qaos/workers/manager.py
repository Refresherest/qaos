"""
QAOS Worker Manager
"""

from .registry import worker_registry

from .default import default_worker


class WorkerManager:

    def __init__(self, registry=None, default=None):

        self._registry = worker_registry if registry is None else registry
        self._default = default_worker if default is None else default

        #
        # Register the default worker
        # once when QAOS starts.
        #

        if self._registry.get(self._default.name) is None:

            self._registry.register(self._default)

    # ---------------------------------

    def register(self, worker):

        self._registry.register(worker)

    # ---------------------------------

    def unregister(self, name):

        self._registry.unregister(name)

    # ---------------------------------

    def get(self, name="default"):

        return self._registry.get(name)

    # ---------------------------------

    def workers(self):

        return self._registry.all()

    # ---------------------------------

    def execute(self, item):

        worker = self.get()

        if worker is None:

            raise RuntimeError(
                "No worker registered."
            )

        return worker.execute(item)


worker_manager = WorkerManager()
