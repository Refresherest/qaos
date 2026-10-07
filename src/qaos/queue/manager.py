"""
QAOS Queue Manager
"""

from copy import deepcopy
from datetime import datetime
import hashlib
import hmac
import os
from threading import Lock
from uuid import uuid4

from qaos.storage import create_stores, DATA

from .item import QueueItem
from .registry import QueueRegistry, queue_registry

from qaos.workers import worker_manager
from qaos.planner import Task


class QueueManager:

    _PILOT_STATES = frozenset({
        "pilot_claimed", "pilot_unknown", "pilot_evidence_recorded",
    })

    def __init__(self, stores=None, registry=None, workers=None, id_generator=None):

        uses_default_stores = stores is None
        self._stores = stores or create_stores(DATA)
        self._registry = registry or (
            queue_registry
            if uses_default_stores
            else QueueRegistry()
        )
        self._workers = worker_manager if workers is None else workers
        self._id_generator = id_generator or (lambda: str(uuid4()))
        self._transactional = callable(getattr(self._stores.queue_db, "transact", None))
        self._release_capabilities = {}
        self._release_lock = Lock()

        self._load()

    # -------------------------------------------------

    def _load(self):

        self._registry.clear()
        seen_ids = set()

        for data in self._stores.queue_db.load():

            queue_item_id = data.get("queue_item_id")
            if queue_item_id is not None:
                if queue_item_id in seen_ids:
                    raise ValueError("duplicate persisted queue_item_id")
                seen_ids.add(queue_item_id)

            self._registry.add(self._item_from_record(data))

    @staticmethod
    def _item_from_record(data):

        action = None

        if data.get("action"):

            action = Task.from_dict(data["action"])

        item = QueueItem(

                objective=data["objective"],

                assignee=data["assignee"],

                action=action,

                objective_id=data.get("objective_id"),

                task_id=data.get("task_id"),

                queue_item_id=data.get("queue_item_id"),

                pilot_attempt=data.get("pilot_attempt"),

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

        return item

    # -------------------------------------------------

    def _save(self):

        if self._transactional:
            raise RuntimeError("blind QueueManager snapshot save is refused for SQLite")

        data = [self._record_from_item(item) for item in self._registry.all()]
        self._stores.queue_db.save(data)

    @staticmethod
    def _record_from_item(item):

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

        if item.queue_item_id is not None:
            record["queue_item_id"] = item.queue_item_id

        if item.pilot_attempt is not None:
            record["pilot_attempt"] = item.pilot_attempt

        return record

    # -------------------------------------------------

    def add(self, item):

        if item.queue_item_id is not None:
            raise ValueError("QueueManager.add requires an unadmitted QueueItem")

        queue_item_id = self._id_generator()
        if not isinstance(queue_item_id, str) or not queue_item_id:
            raise ValueError("generated queue_item_id is invalid")
        if any(
            row.queue_item_id == queue_item_id for row in self._registry.all()
        ):
            raise ValueError("duplicate queue_item_id")

        if self._transactional:
            record = self._record_from_item(item)
            record["queue_item_id"] = queue_item_id

            def append_if_unclaimed(records):
                if any(row.get("queue_item_id") == queue_item_id for row in records):
                    raise ValueError("duplicate queue_item_id")
                if item.objective_id is not None and any(
                    row.get("objective_id") == item.objective_id
                    and row.get("pilot_attempt") is not None
                    for row in records
                ):
                    raise ValueError("pilot Objective is held; alias add refused")
                records.append(record)

            self._stores.queue_db.transact(append_if_unclaimed)
            item._assign_identity(queue_item_id)
            self._load()
            return

        item._assign_identity(queue_item_id)

        self._registry.add(item)

        self._save()

    # -------------------------------------------------

    def items(self):

        if self._transactional:
            self._load()

        return self._registry.all()

    @staticmethod
    def _one_record(records, queue_item_id):
        matches = [row for row in records if row.get("queue_item_id") == queue_item_id]
        if len(matches) != 1:
            raise ValueError("QueueItem identity is missing or ambiguous")
        return matches[0]

    @staticmethod
    def _has_pilot_attempt(row):
        return row.get("pilot_attempt") is not None or row.get("status") in QueueManager._PILOT_STATES

    def _require_transactional(self):
        if not self._transactional:
            raise RuntimeError("durable pilot authority requires the explicit SQLite queue")

    def get_pilot_claim(self, queue_item_id):
        self._require_transactional()
        row = self._one_record(self._stores.queue_db.load(), queue_item_id)
        if not self._has_pilot_attempt(row) or not isinstance(row.get("pilot_attempt"), dict):
            raise ValueError("QueueItem has no durable pilot claim")
        return {"status": row["status"], "pilot_attempt": deepcopy(row["pilot_attempt"])}

    def claim_pilot(self, queue_item_id, envelope):
        """Commit one frozen request in the canonical queue before any send."""
        self._require_transactional()
        if not isinstance(queue_item_id, str) or not queue_item_id:
            raise ValueError("pilot QueueItem identity is missing")
        if not isinstance(envelope, dict) or set(envelope) != {
            "queue_item_id", "objective_id", "task_id", "candidate_artifact",
            "acceptance_artifact", "request", "request_sha256", "claimed_at",
        }:
            raise ValueError("pilot attempt envelope has invalid fields")
        request = envelope["request"]
        from qaos.workers.durable_pilot import validate_frozen_request_schema
        request_bytes = validate_frozen_request_schema(request)
        if hashlib.sha256(request_bytes).hexdigest() != envelope["request_sha256"]:
            raise ValueError("pilot request digest or bounds are invalid")
        if (
            envelope["queue_item_id"] != queue_item_id
            or envelope["objective_id"] != request.get("objective_id")
            or envelope["task_id"] != request.get("task_id")
            or envelope["candidate_artifact"] != request.get("candidate_artifact")
            or envelope["acceptance_artifact"] != request.get("acceptance_artifact")
            or not isinstance(request.get("request_id"), str)
            or not request["request_id"]
            or not isinstance(request.get("nonce"), str)
            or not request["nonce"]
            or not isinstance(envelope["claimed_at"], str)
            or not envelope["claimed_at"]
        ):
            raise ValueError("pilot request and envelope do not correlate")

        frozen = deepcopy(envelope)

        def claim(records):
            row = self._one_record(records, queue_item_id)
            objective_id = row.get("objective_id")
            task_id = row.get("task_id")
            if (
                row.get("status") != "pending"
                or row.get("result") is not None
                or self._has_pilot_attempt(row)
                or not objective_id or not task_id
                or row.get("action") is None
                or row["action"].get("task_id") != task_id
                or objective_id != frozen["objective_id"]
                or task_id != frozen["task_id"]
            ):
                raise ValueError("pilot origin is not a fresh identified pending QueueItem")
            if sum(
                other.get("objective_id") == objective_id
                and other.get("task_id") == task_id
                for other in records
            ) != 1:
                raise ValueError("ambiguous pilot QueueItem origin")
            if any(
                other is not row and other.get("objective_id") == objective_id
                and (self._has_pilot_attempt(other) or other.get("status") == "running")
                for other in records
            ):
                raise ValueError("pilot Objective has another attempt or running work")
            row["status"] = "pilot_claimed"
            row["pilot_attempt"] = frozen

        self._stores.queue_db.transact(claim)
        self._load()
        capability = os.urandom(32)
        with self._release_lock:
            self._release_capabilities[queue_item_id] = capability
        return capability

    def mark_pilot_unknown(self, queue_item_id):
        self._require_transactional()
        with self._release_lock:
            self._release_capabilities.pop(queue_item_id, None)

        def hold(records):
            row = self._one_record(records, queue_item_id)
            if not isinstance(row.get("pilot_attempt"), dict):
                raise ValueError("QueueItem has no pilot attempt")
            if row["status"] == "pilot_claimed":
                row["status"] = "pilot_unknown"
            elif row["status"] != "pilot_unknown":
                raise ValueError("pilot attempt cannot become unknown from this state")

        self._stores.queue_db.transact(hold)
        self._load()

    def consume_pilot_send_authority(self, queue_item_id, envelope, capability):
        """Single atomic byte-release gate; uncertain state precedes release.

        The caller must still be a separately authorized original transport.
        This method opens no connection and returns no bytes itself.
        """
        self._require_transactional()
        with self._release_lock:
            original = self._release_capabilities.pop(queue_item_id, None)
        if (
            not isinstance(capability, bytes)
            or original is None
            or not hmac.compare_digest(original, capability)
        ):
            raise ValueError("pilot release requires the original volatile claim capability")

        def consume(records):
            row = self._one_record(records, queue_item_id)
            if (
                row.get("status") != "pilot_claimed"
                or row.get("pilot_attempt") != envelope
                or row.get("result") is not None
            ):
                raise ValueError("pilot send authority is already consumed or changed")
            row["status"] = "pilot_unknown"

        self._stores.queue_db.transact(consume)
        self._load()

    def ensure_dispatchable_objective(self, objective_id):
        """Read fresh authority before a higher-level lifecycle transition."""
        if self._transactional:
            records = self._stores.queue_db.load()
        else:
            records = [self._record_from_item(item) for item in self._registry.all()]
        if any(
            row.get("objective_id") == objective_id and self._has_pilot_attempt(row)
            for row in records
        ):
            raise ValueError("pilot Objective is held for separate adjudication")

    # -------------------------------------------------

    def process(self):

        if self._transactional:
            return self._process_transactional()

        worker = self._workers.get(
            "default"
        )

        failed_objective_ids = {
            item.objective_id
            for item in self._registry.all()
            if item.objective_id is not None and (
                item.status == "failed" or item.pilot_attempt is not None
                or item.status in self._PILOT_STATES
            )
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

    def _process_transactional(self):
        worker = self._workers.get("default")
        if worker is None:
            raise RuntimeError("No worker registered.")

        while True:
            def reserve_next(records):
                blocked = {
                    row.get("objective_id") for row in records
                    if row.get("objective_id") is not None and (
                        row.get("status") in {"failed", "running"}
                        or self._has_pilot_attempt(row)
                        or row.get("queue_item_id") is None
                    )
                }
                for row in records:
                    if row.get("status") != "pending":
                        continue
                    if row.get("objective_id") in blocked:
                        continue
                    if row.get("queue_item_id") is None:
                        continue  # legacy rows have no safe dispatch identity
                    row["status"] = "running"
                    row["started"] = datetime.now().isoformat()
                    return deepcopy(row)
                return None

            reserved = self._stores.queue_db.transact(reserve_next)
            if reserved is None:
                self._load()
                return

            item = self._item_from_record(reserved)
            worker_error = None
            try:
                worker.execute(item)
                if item.status not in {"completed", "failed"}:
                    raise RuntimeError("worker did not produce a terminal QueueItem state")
            except Exception as error:
                worker_error = error
                if item.status != "failed":
                    item.status = "failed"
                    item.completed = datetime.now()
                if item.action is not None and item.action.status == "running":
                    item.action.fail()

            final_record = self._record_from_item(item)

            def finish(records):
                row = self._one_record(records, item.queue_item_id)
                if row.get("status") != "running" or self._has_pilot_attempt(row):
                    raise RuntimeError("reserved QueueItem changed before result commit")
                if row != reserved:
                    raise RuntimeError("reserved QueueItem changed before result commit")
                row.clear()
                row.update(final_record)

            try:
                self._stores.queue_db.transact(finish)
            except Exception:
                self._load()
                if worker_error is not None:
                    raise worker_error
                raise
            self._load()
            if worker_error is not None:
                raise worker_error

    # -------------------------------------------------

    def validate_recovery(self, objective_id):

        if not isinstance(objective_id, str) or not objective_id:
            raise ValueError("objective_id must be a non-empty string")

        if self._transactional:
            self._load()

        items = [
            item
            for item in self._registry.all()
            if item.objective_id == objective_id
        ]

        return self._validate_recovery_items(items)

    @staticmethod
    def _validate_recovery_items(items):

        if not items:
            raise ValueError("no QueueItems found for objective_id")

        if any(
            item.pilot_attempt is not None or item.status in QueueManager._PILOT_STATES
            for item in items
        ):
            raise ValueError("pilot Objective is held from generic recovery")

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

        if self._transactional:
            return self._recover_transactional(objective_id, canonical_tasks)

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

    def _recover_transactional(self, objective_id, canonical_tasks):
        targets = self.validate_recovery(objective_id)
        worker = self._workers.get("default")
        if worker is None:
            raise RuntimeError("No worker registered.")
        if set(canonical_tasks) != {item.task_id for item in targets}:
            raise ValueError("canonical recovery Tasks do not match QueueItems")
        target_ids = [item.queue_item_id for item in targets]
        if any(identity is None for identity in target_ids):
            raise ValueError("legacy QueueItem cannot be transactionally recovered")

        def reserve(records):
            current = self._validate_recovery_items([
                self._item_from_record(row)
                for row in records if row.get("objective_id") == objective_id
            ])
            if [item.queue_item_id for item in current] != target_ids:
                raise ValueError("recovery targets changed before reservation")
            reserved = []
            for index, queue_item_id in enumerate(target_ids):
                row = self._one_record(records, queue_item_id)
                if index == 0:
                    row["result"] = None
                    row["started"] = None
                    row["completed"] = None
                    row["action"]["status"] = "pending"
                    row["action"]["started"] = None
                    row["action"]["completed"] = None
                row["status"] = "running"
                row["started"] = datetime.now().isoformat()
                reserved.append(deepcopy(row))
            return reserved

        reserved = self._stores.queue_db.transact(reserve)
        executed = []
        for index, record in enumerate(reserved):
            item = self._item_from_record(record)
            canonical_task = canonical_tasks[item.task_id]
            worker_error = None
            try:
                worker.execute(item)
                if item.status not in {"completed", "failed"}:
                    raise RuntimeError("worker did not produce a terminal QueueItem state")
            except Exception as error:
                worker_error = error
                if item.status != "failed":
                    item.status = "failed"
                    item.completed = datetime.now()
                if item.action.status == "running":
                    item.action.fail()

            final_record = self._record_from_item(item)

            def finish(records):
                row = self._one_record(records, item.queue_item_id)
                if row.get("status") != "running" or self._has_pilot_attempt(row):
                    raise RuntimeError("reserved recovery QueueItem changed")
                if row != record:
                    raise RuntimeError("reserved recovery QueueItem changed")
                row.clear()
                row.update(final_record)
                if worker_error is not None:
                    for remaining in reserved[index + 1:]:
                        waiting = self._one_record(records, remaining["queue_item_id"])
                        if waiting.get("status") != "running":
                            raise RuntimeError("unexecuted recovery QueueItem changed")
                        waiting["status"] = "pending"
                        waiting["started"] = None

            try:
                self._stores.queue_db.transact(finish)
            finally:
                canonical_task.status = item.action.status
                canonical_task.started = item.action.started
                canonical_task.completed = item.action.completed
            executed.append(item)
            if worker_error is not None:
                self._load()
                raise worker_error
        self._load()
        return tuple(executed)

    # -------------------------------------------------

    def clear(self):

        if self._transactional:
            def clear_if_stable(records):
                if any(
                    self._has_pilot_attempt(row)
                    or row.get("status") not in {"pending", "completed", "failed"}
                    for row in records
                ):
                    raise ValueError("attempted or active QueueItem cannot be cleared")
                records.clear()

            self._stores.queue_db.transact(clear_if_stable, allow_delete=True)
            self._load()
            return

        self._registry.clear()

        self._save()

    # -------------------------------------------------

    def save(self):

        self._save()


queue_manager = QueueManager()
