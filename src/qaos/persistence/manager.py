"""
QAOS Persistence Manager
"""

from qaos.persistence.registry import (
    register,
    unregister,
    get,
    all_stores,
)


class PersistenceManager:

    # -------------------------------------------------

    def register(self, store):

        register(store)

    # -------------------------------------------------

    def unregister(self, name):

        unregister(name)

    # -------------------------------------------------

    def get(self, name):

        return get(name)

    # -------------------------------------------------

    def stores(self):

        return all_stores()

    # -------------------------------------------------

    def initialize(self):

        for store in all_stores().values():

            if hasattr(
                store,
                "initialize",
            ):

                store.initialize()

    # -------------------------------------------------

    def save(self):
        """
        Persist every registered store.

        Stores that expose a save()
        method will be asked to
        persist themselves.
        """

        for store in all_stores().values():

            if hasattr(
                store,
                "save",
            ):

                store.save()

    # -------------------------------------------------

    def shutdown(self):

        #
        # Persist before shutdown.
        #

        self.save()

        for store in all_stores().values():

            if hasattr(
                store,
                "shutdown",
            ):

                store.shutdown()


persistence_manager = PersistenceManager()