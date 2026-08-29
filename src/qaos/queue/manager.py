"""
QAOS Queue Manager
"""

from datetime import datetime

from qaos.storage import create_stores, DATA

from .item import QueueItem
from .registry import QueueRegistry, queue_registry

from qaos.workers import worker_manager
from qaos.planner import Task


class QueueManager:

    def __init__(self, stores=None, registry=None, workers=None):

        uses_default_stores = stores is None
        self._stores = stores or create_stores(DATA)
        self._registry = registry or (
            queue_registry
            if uses_default_stores
            else QueueRegistry()
        )
        self._workers = worker_manager if workers is None else workers

        self._load()

    # -------------------------------------------------

    def _load(self):

        self._registry.clear()

        for data in self._stores.queue_db.load():

            action = None

            if data.get("action"):

                action = Task.from_dict(
                    data["action"]
                )

            item = QueueItem(

                objective=data["objective"],

                assignee=data["assignee"],

                action=action,

            )

            item.status = data.get(
                "status",
                "pending",
            )

            item.result = data.get(
                "result"
            )

            started = data.get(
                "started"
            )

            completed = data.get(
                "completed"
            )

            item.started = (
                datetime.fromisoformat(started)
                if started
                else None
            )

            item.completed = (
                datetime.fromisoformat(completed)
                if completed
                else None
            )

            self._registry.add(item)

    # -------------------------------------------------

    def _save(self):

        data = []

        for item in self._registry.all():

            action = None

            if item.action:

                action = item.action.to_dict()

            data.append({

                "objective": item.objective,

                "assignee": item.assignee,

                "action": action,

                "status": item.status,

                "result": item.result,

                "started": (
                    item.started.isoformat()
                    if item.started
                    else None
                ),

                "completed": (
                    item.completed.isoformat()
                    if item.completed
                    else None
                ),

            })

        self._stores.queue_db.save(data)

    # -------------------------------------------------

    def add(self, item):

        self._registry.add(item)

        self._save()

    # -------------------------------------------------

    def items(self):

        return self._registry.all()

    # -------------------------------------------------

    def process(self):

        worker = self._workers.get(
            "default"
        )

        try:
            for item in self._registry.all():

                if item.status != "pending":
                    continue

                worker.execute(item)
        finally:
            self._save()

    # -------------------------------------------------

    def clear(self):

        self._registry.clear()

        self._save()

    # -------------------------------------------------

    def save(self):

        self._save()


queue_manager = QueueManager()
