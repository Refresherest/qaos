"""
QAOS Database
"""

from .json_store import JSONStore
from .paths import DATA, path_for


class Stores:
    """Explicit storage collection bound to a single data directory."""

    def __init__(self, data_dir):

        self.data_dir = data_dir

        self.memory_db = JSONStore(
            path_for(data_dir, "memory"),
        )

        self.knowledge_db = JSONStore(
            path_for(data_dir, "knowledge"),
        )

        self.artifact_db = JSONStore(
            path_for(data_dir, "artifacts"),
        )

        self.objective_db = JSONStore(
            path_for(data_dir, "objectives"),
        )

        self.reflection_db = JSONStore(
            path_for(data_dir, "reflections"),
        )

        self.event_db = JSONStore(
            path_for(data_dir, "events"),
        )

        self.plan_db = JSONStore(
            path_for(data_dir, "plans"),
        )

        self.queue_db = JSONStore(
            path_for(data_dir, "queue"),
        )


def create_stores(data_dir):
    """Construct the explicit storage collection for data_dir.

    This is the active storage construction boundary; JSONStore instances
    are created here rather than at module import time.
    """
    return Stores(data_dir)