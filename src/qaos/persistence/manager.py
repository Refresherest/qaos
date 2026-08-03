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

    def register(self, store):
        register(store)

    def unregister(self, name):
        unregister(name)

    def get(self, name):
        return get(name)

    def stores(self):
        return all_stores()

    def initialize(self):
        for store in all_stores().values():
            store.initialize()

    def shutdown(self):
        for store in all_stores().values():
            store.shutdown()


persistence_manager = PersistenceManager()