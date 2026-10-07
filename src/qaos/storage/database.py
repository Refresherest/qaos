"""
QAOS Database
"""

from pathlib import Path

from .json_store import JSONStore
from .paths import DATA, path_for
from .sqlite_queue_store import SQLiteQueueStore, QueueStoreConflictError


class Stores:
    """Explicit storage collection bound to a single data directory."""

    def __init__(self, data_dir, *, queue_backend="json"):

        self.data_dir = data_dir

        if queue_backend not in {"json", "sqlite"}:
            raise ValueError("queue_backend must be 'json' or 'sqlite'")
        self.queue_backend = queue_backend

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

        sqlite_path = Path(data_dir) / "queue.sqlite3"
        if queue_backend == "json":
            if sqlite_path.exists():
                raise QueueStoreConflictError(
                    "queue.sqlite3 exists; JSON and SQLite queue authority cannot coexist"
                )
            self.queue_db = JSONStore(path_for(data_dir, "queue"))
        else:
            self.queue_db = SQLiteQueueStore(sqlite_path)


def create_stores(data_dir, *, queue_backend="json"):
    """Construct the explicit storage collection for data_dir.

    JSON remains the default.  SQLite queue persistence is explicitly opt-in
    for an isolated, fresh local workspace; it never migrates active data.
    """
    return Stores(data_dir, queue_backend=queue_backend)
