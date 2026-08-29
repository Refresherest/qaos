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

                objective_id=data.get("objective_id"),

                task_id=data.get("task_id"),

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

            record = {

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

            }

            if item.objective_id is not None:
                record["objective_id"] = item.objective_id

            if item.task_id is not None:
                record["task_id"] = item.task_id

            data.append(record)

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

        failed_objective_ids = {
            item.objective_id
            for item in self._registry.all()
            if item.objective_id is not None and item.status == "failed"
        }

        try:
            for item in self._registry.all():

                if item.status != "pending":
                    continue

                if item.objective_id in failed_objective_ids:
                    continue

                worker.execute(item)
        finally:
            self._save()

    # -------------------------------------------------

    def validate_recovery(self, objective_id):

        if not isinstance(objective_id, str) or not objective_id:
            raise ValueError("objective_id must be a non-empty string")

        items = [
            item
            for item in self._registry.all()
            if item.objective_id == objective_id
        ]

        if not items:
            raise ValueError("no QueueItems found for objective_id")

        allowed = {"pending", "completed", "failed"}
        if any(item.status not in allowed for item in items):
            raise ValueError("recovery requires stable QueueItem statuses")

        failed_indexes = [
            index
            for index, item in enumerate(items)
            if item.status == "failed"
        ]

        if len(failed_indexes) != 1:
            raise ValueError("recovery requires exactly one failed QueueItem")

        failed_index = failed_indexes[0]
        if any(item.status == "pending" for item in items[:failed_index]):
            raise ValueError("pending QueueItem precedes the failed QueueItem")

        failed_item = items[failed_index]
        targets = (failed_item,) + tuple(
            item
            for item in items[failed_index + 1:]
            if item.status == "pending"
        )

        task_ids = []
        for item in targets:
            if item.action is None or item.task_id is None:
                raise ValueError("recovery targets require identified actions")
            if item.action.task_id != item.task_id:
                raise ValueError("QueueItem action identity does not match task_id")
            task_ids.append(item.task_id)

        if len(set(task_ids)) != len(task_ids):
            raise ValueError("recovery target task_ids must be unique")

        return targets

    # -------------------------------------------------

    def recover(self, objective_id, canonical_tasks):

        targets = self.validate_recovery(objective_id)
        worker = self._workers.get("default")

        if worker is None:
            raise RuntimeError("No worker registered.")

        if set(canonical_tasks) != {item.task_id for item in targets}:
            raise ValueError("canonical recovery Tasks do not match QueueItems")

        failed_item = targets[0]
        failed_task = canonical_tasks[failed_item.task_id]

        failed_item.status = "pending"
        failed_item.result = None
        failed_item.started = None
        failed_item.completed = None

        for task in {failed_item.action, failed_task}:
            task.status = "pending"
            task.started = None
            task.completed = None

        try:
            for item in targets:
                canonical_task = canonical_tasks[item.task_id]
                try:
                    worker.execute(item)
                finally:
                    canonical_task.status = item.action.status
                    canonical_task.started = item.action.started
                    canonical_task.completed = item.action.completed
        except Exception:
            try:
                self._save()
            except Exception:
                pass
            raise
        else:
            self._save()

        return targets

    # -------------------------------------------------

    def clear(self):

        self._registry.clear()

        self._save()

    # -------------------------------------------------

    def save(self):

        self._save()


queue_manager = QueueManager()
