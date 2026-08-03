"""
QAOS Persistence Manager
"""

from .registry import get


class PersistenceManager:

    def save(self, backend, key, value):
        db = get(backend)

        if db is None:
            raise ValueError(
                f"Unknown persistence backend: {backend}"
            )

        db.save(key, value)

    def load(self, backend, key):
        db = get(backend)

        if db is None:
            raise ValueError(
                f"Unknown persistence backend: {backend}"
            )

        return db.load(key)

    def delete(self, backend, key):
        db = get(backend)

        if db is None:
            raise ValueError(
                f"Unknown persistence backend: {backend}"
            )

        db.delete(key)

    def all(self, backend):
        db = get(backend)

        if db is None:
            raise ValueError(
                f"Unknown persistence backend: {backend}"
            )

        return db.all()


persistence_manager = PersistenceManager()