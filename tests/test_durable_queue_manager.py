"""Fresh-workspace queue authority tests for the local-only WO-178 pilot.

The synthetic request headers below are transaction probes, not worker input.
No test opens transport, runs candidate code, or touches active queue data.
"""

from __future__ import annotations

import base64
import hashlib
import json
import multiprocessing
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest

from qaos.execution.engine import ExecutionEngine
from qaos.execution.manager import ExecutionManager
from qaos.execution.registry import ExecutionRegistry
from qaos.objectives import Objective
from qaos.planner import Task
from qaos.queue import QueueItem, QueueManager
from qaos.storage import create_stores
from qaos.storage.sqlite_queue_store import QueueStoreConflictError
from qaos.workers.durable_pilot import PILOT_RUNTIME_PINS


def _queue(tmp_path: Path, *, workers=None, id_generator=None) -> QueueManager:
    return QueueManager(
        stores=create_stores(tmp_path, queue_backend="sqlite"),
        workers=workers,
        id_generator=id_generator,
    )


def _add(
    manager: QueueManager,
    objective_id: str,
    task_id: str,
) -> QueueItem:
    task = Task(f"Synthetic task {task_id}", task_id=task_id)
    item = QueueItem(
        f"Synthetic objective {objective_id}",
        "default",
        action=task,
        objective_id=objective_id,
    )
    manager.add(item)
    return item


def _envelope(
    item: QueueItem,
    *,
    request_id: str = "123e4567-e89b-42d3-a456-426614174000",
) -> dict:
    candidate = {"artifact_id": "candidate-1", "content_sha256": "a" * 64}
    acceptance = {"artifact_id": "acceptance-1", "content_sha256": "b" * 64}
    request = {
        "protocol": "qaos.worker.validation",
        "version": 1,
        "request_id": request_id,
        "nonce": base64.urlsafe_b64encode(b"n" * 32).decode().rstrip("="),
        "created_at": "2026-10-04T12:00:00Z",
        "expires_at": "2026-10-04T12:02:00Z",
        "objective_id": item.objective_id,
        "task_id": item.task_id,
        "candidate_artifact": candidate,
        "acceptance_artifact": acceptance,
        "members": [
            {"role": "acceptance", "path": "acceptance/acceptance.py", "size": 1, "sha256": "b" * 64},
            {"role": "candidate", "path": "candidate/candidate.py", "size": 1, "sha256": "a" * 64},
        ],
        "runtime": dict(PILOT_RUNTIME_PINS),
    }
    encoded = json.dumps(
        request, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return {
        "queue_item_id": item.queue_item_id,
        "objective_id": item.objective_id,
        "task_id": item.task_id,
        "candidate_artifact": candidate,
        "acceptance_artifact": acceptance,
        "request": request,
        "request_sha256": hashlib.sha256(encoded).hexdigest(),
        "claimed_at": "2026-10-04T12:00:00Z",
    }


def _claim_in_process(
    workspace: str,
    queue_item_id: str,
    envelope: dict,
    release,
    outcomes,
) -> None:
    manager = _queue(Path(workspace))
    outcomes.put("ready")
    if not release.wait(15):
        outcomes.put("timed-out")
        return
    try:
        manager.claim_pilot(queue_item_id, envelope)
    except (ValueError, QueueStoreConflictError) as error:
        outcomes.put(("refused", type(error).__name__))
    else:
        outcomes.put(("claimed", queue_item_id))


class _Workers:
    def __init__(self, *, fail_task_id: str | None = None):
        self.calls: list[str] = []
        self.fail_task_id = fail_task_id

    def get(self, name: str):
        assert name == "default"
        return self

    def execute(self, item: QueueItem) -> None:
        self.calls.append(item.task_id)
        item.action.start()
        if item.task_id == self.fail_task_id:
            raise RuntimeError("synthetic worker failure")
        item.action.complete()
        item.status = "completed"
        item.result = "synthetic completion"


def test_new_identity_is_immutable_and_legacy_identity_is_not_inferred(tmp_path):
    workspace = tmp_path / "fresh-queue"
    stores = create_stores(workspace, queue_backend="sqlite")
    manager = QueueManager(stores=stores, id_generator=lambda: "queue-new")
    new_item = _add(manager, "objective-new", "task-new")
    assert new_item.queue_item_id == "queue-new"
    with pytest.raises(ValueError, match="immutable"):
        new_item._assign_identity("queue-other")
    assert _queue(workspace).items()[0].queue_item_id == "queue-new"

    legacy_workspace = tmp_path / "legacy-fixture"
    legacy_stores = create_stores(legacy_workspace, queue_backend="sqlite")
    legacy_stores.queue_db.import_legacy_snapshot([
        {
            "objective": "Legacy fixture",
            "objective_id": "objective-legacy",
            "assignee": "default",
            "action": Task("Legacy", task_id="task-legacy").to_dict(),
            "task_id": "task-legacy",
            "status": "pending",
            "result": None,
            "started": None,
            "completed": None,
        }
    ])
    legacy = QueueManager(stores=legacy_stores).items()[0]
    assert legacy.queue_item_id is None
    invented = QueueItem(
        legacy.objective,
        legacy.assignee,
        action=legacy.action,
        objective_id=legacy.objective_id,
        queue_item_id="invented-id",
    )
    with pytest.raises(ValueError, match="identity"):
        QueueManager(stores=legacy_stores).claim_pilot(
            "invented-id", _envelope(invented)
        )
    assert legacy_stores.queue_db.load()[0].get("queue_item_id") is None


def test_competing_processes_commit_only_one_pilot_claim(tmp_path):
    workspace = tmp_path / "two-processes"
    manager = _queue(workspace, id_generator=lambda: "queue-race")
    item = _add(manager, "objective-race", "task-race")
    envelope = _envelope(item)
    context = multiprocessing.get_context("spawn")
    release = context.Event()
    outcomes = context.Queue()
    children = [
        context.Process(
            target=_claim_in_process,
            args=(str(workspace), item.queue_item_id, envelope, release, outcomes),
        )
        for _ in range(2)
    ]
    for child in children:
        child.start()
    try:
        assert [outcomes.get(timeout=20) for _ in children] == ["ready", "ready"]
        release.set()
        results = [outcomes.get(timeout=20) for _ in children]
        assert sum(result[0] == "claimed" for result in results) == 1
        assert sum(result[0] == "refused" for result in results) == 1
    finally:
        release.set()
        for child in children:
            child.join(timeout=20)
            if child.is_alive():
                child.terminate()
                child.join(timeout=5)
    assert all(child.exitcode == 0 for child in children)
    saved = _queue(workspace).items()
    assert len(saved) == 1
    assert saved[0].status == "pilot_claimed"
    assert saved[0].pilot_attempt == envelope
    assert saved[0].result is None


def test_stale_manager_and_direct_store_cannot_blindly_save_claim(tmp_path):
    workspace = tmp_path / "stale"
    first = _queue(workspace, id_generator=lambda: "queue-stale")
    item = _add(first, "objective-stale", "task-stale")
    stale = _queue(workspace)
    stale_snapshot = stale._stores.queue_db.load()
    first.claim_pilot(item.queue_item_id, _envelope(item))

    with pytest.raises(RuntimeError, match="blind.*save"):
        stale.save()
    with pytest.raises(QueueStoreConflictError, match="blind.*save"):
        stale._stores.queue_db.save(stale_snapshot)
    assert _queue(workspace).items()[0].status == "pilot_claimed"


def test_direct_claim_api_rejects_extra_request_data_before_commit(tmp_path):
    workspace = tmp_path / "strict-header"
    manager = _queue(workspace, id_generator=lambda: "queue-strict")
    item = _add(manager, "objective-strict", "task-strict")
    envelope = _envelope(item)
    envelope["request"]["credential"] = "synthetic-forbidden-field"
    encoded = json.dumps(
        envelope["request"], ensure_ascii=False, sort_keys=True,
        separators=(",", ":"),
    ).encode()
    envelope["request_sha256"] = hashlib.sha256(encoded).hexdigest()
    with pytest.raises(ValueError, match="request fields"):
        manager.claim_pilot(item.queue_item_id, envelope)
    assert manager.items()[0].status == "pending"


def test_claim_rejects_ambiguous_origin_and_later_alias(tmp_path):
    ambiguous_workspace = tmp_path / "ambiguous"
    ambiguous = _queue(ambiguous_workspace, id_generator=iter(("queue-a", "queue-b")).__next__)
    first = _add(ambiguous, "objective-shared", "task-shared")
    _add(ambiguous, "objective-shared", "task-shared")
    with pytest.raises(ValueError, match="ambiguous"):
        ambiguous.claim_pilot(first.queue_item_id, _envelope(first))
    assert all(item.status == "pending" for item in ambiguous.items())

    workspace = tmp_path / "later-alias"
    manager = _queue(
        workspace,
        id_generator=iter(("queue-origin", "queue-alias-1", "queue-alias-2")).__next__,
    )
    claimed = _add(manager, "objective-held", "task-origin")
    manager.claim_pilot(claimed.queue_item_id, _envelope(claimed))
    with pytest.raises(ValueError, match="held"):
        _add(manager, "objective-held", "task-origin")
    with pytest.raises(ValueError, match="held"):
        _add(manager, "objective-held", "task-sibling")
    assert len(manager.items()) == 1


def test_process_holds_same_objective_siblings_but_executes_unrelated(tmp_path):
    workspace = tmp_path / "sibling-hold"
    workers = _Workers()
    manager = _queue(
        workspace,
        workers=workers,
        id_generator=iter(("queue-pilot", "queue-sibling", "queue-other")).__next__,
    )
    pilot = _add(manager, "objective-held", "task-pilot")
    _add(manager, "objective-held", "task-sibling")
    _add(manager, "objective-other", "task-other")
    manager.claim_pilot(pilot.queue_item_id, _envelope(pilot))

    manager.process()

    assert workers.calls == ["task-other"]
    assert {item.task_id: item.status for item in manager.items()} == {
        "task-pilot": "pilot_claimed",
        "task-sibling": "pending",
        "task-other": "completed",
    }
    manager.mark_pilot_unknown(pilot.queue_item_id)
    manager.process()
    assert workers.calls == ["task-other"]


def test_stale_manager_selection_observes_new_claim_before_worker_call(tmp_path):
    workspace = tmp_path / "stale-dispatch"
    owner = _queue(
        workspace,
        id_generator=iter(("queue-origin", "queue-sibling", "queue-other")).__next__,
    )
    pilot = _add(owner, "objective-held", "task-origin")
    _add(owner, "objective-held", "task-sibling")
    _add(owner, "objective-other", "task-other")
    workers = _Workers()
    stale = _queue(workspace, workers=workers)
    owner.claim_pilot(pilot.queue_item_id, _envelope(pilot))

    stale.process()

    assert workers.calls == ["task-other"]
    assert {item.task_id: item.status for item in stale.items()} == {
        "task-origin": "pilot_claimed",
        "task-sibling": "pending",
        "task-other": "completed",
    }


def test_competing_generic_processors_reserve_one_item_once(tmp_path):
    workspace = tmp_path / "generic-race"
    owner = _queue(workspace, id_generator=lambda: "queue-once")
    _add(owner, "objective-once", "task-once")
    entered = threading.Event()
    release = threading.Event()
    calls = []

    class HoldingWorker:
        def get(self, name):
            assert name == "default"
            return self

        def execute(self, item):
            calls.append(item.task_id)
            entered.set()
            assert release.wait(10)
            item.status = "completed"
            item.action.complete()
            item.result = "synthetic completion"

    worker = HoldingWorker()
    first = _queue(workspace, workers=worker)
    second = _queue(workspace, workers=worker)
    with ThreadPoolExecutor(max_workers=2) as pool:
        future = pool.submit(first.process)
        assert entered.wait(10)
        second.process()
        release.set()
        future.result(timeout=10)
    assert calls == ["task-once"]
    assert _queue(workspace).items()[0].status == "completed"


def test_generic_result_commit_refuses_concurrent_row_drift(tmp_path):
    workspace = tmp_path / "finalizer-drift"
    owner = _queue(workspace, id_generator=lambda: "queue-drift")
    _add(owner, "objective-drift", "task-drift")
    store = owner._stores.queue_db

    class DriftingWorker:
        def get(self, name):
            return self

        def execute(self, item):
            store.transact(lambda rows: rows[0].update(result="concurrent edit"))
            item.status = "completed"
            item.action.complete()
            item.result = "worker result"

    manager = _queue(workspace, workers=DriftingWorker())
    with pytest.raises(RuntimeError, match="reserved QueueItem changed"):
        manager.process()
    row = store.load()[0]
    assert row["status"] == "running"
    assert row["result"] == "concurrent edit"


def test_unrelated_generic_recovery_still_works_after_pilot_claim(tmp_path):
    workspace = tmp_path / "unrelated-recovery"
    workers = _Workers()
    manager = _queue(
        workspace, workers=workers,
        id_generator=iter(("queue-pilot", "queue-failed", "queue-pending")).__next__,
    )
    pilot = _add(manager, "objective-pilot", "task-pilot")
    failed = _add(manager, "objective-other", "task-failed")
    _add(manager, "objective-other", "task-pending")
    manager.claim_pilot(pilot.queue_item_id, _envelope(pilot))

    def seed_failed(records):
        row = next(row for row in records if row.get("queue_item_id") == failed.queue_item_id)
        row["status"] = "failed"
        row["action"]["status"] = "failed"

    manager._stores.queue_db.transact(seed_failed)
    canonical = {
        task_id: Task(f"Canonical {task_id}", task_id=task_id)
        for task_id in ("task-failed", "task-pending")
    }
    recovered = manager.recover("objective-other", canonical)

    assert [item.task_id for item in recovered] == ["task-failed", "task-pending"]
    assert workers.calls == ["task-failed", "task-pending"]
    assert {item.task_id: item.status for item in manager.items()} == {
        "task-pilot": "pilot_claimed",
        "task-failed": "completed",
        "task-pending": "completed",
    }


def test_generic_recovery_refuses_whole_objective_with_attempted_pilot(tmp_path):
    workspace = tmp_path / "recovery-hold"
    workers = _Workers(fail_task_id="task-failed")
    manager = _queue(
        workspace,
        workers=workers,
        id_generator=iter(("queue-failed", "queue-pilot")).__next__,
    )
    _add(manager, "objective-recover", "task-failed")
    with pytest.raises(RuntimeError, match="synthetic worker failure"):
        manager.process()
    pilot = _add(manager, "objective-recover", "task-pilot")
    manager.claim_pilot(pilot.queue_item_id, _envelope(pilot))

    with pytest.raises(ValueError, match="pilot Objective.*recovery"):
        manager.validate_recovery("objective-recover")
    with pytest.raises(ValueError, match="pilot Objective.*recovery"):
        manager.recover("objective-recover", {"task-failed": Task("canonical", task_id="task-failed")})
    assert workers.calls == ["task-failed"]


def test_clear_refuses_attempt_and_claim_survives_reopen_without_retry(tmp_path):
    workspace = tmp_path / "reopen-hold"
    workers = _Workers()
    manager = _queue(workspace, id_generator=lambda: "queue-held")
    item = _add(manager, "objective-held", "task-held")
    envelope = _envelope(item)
    manager.claim_pilot(item.queue_item_id, envelope)

    restarted = _queue(workspace, workers=workers)
    with pytest.raises(ValueError, match="cannot be cleared"):
        restarted.clear()
    with pytest.raises(ValueError, match="fresh.*pending"):
        restarted.claim_pilot(
            item.queue_item_id,
            _envelope(item, request_id="123e4567-e89b-42d3-a456-426614174001"),
        )
    restarted.process()
    assert workers.calls == []
    assert restarted.items()[0].pilot_attempt == envelope
    restarted.mark_pilot_unknown(item.queue_item_id)
    after_unknown = _queue(workspace, workers=workers)
    after_unknown.process()
    assert workers.calls == []
    assert after_unknown.items()[0].status == "pilot_unknown"
    assert after_unknown.items()[0].result is None


def test_restarted_manager_cannot_reconstruct_byte_release_capability(tmp_path):
    workspace = tmp_path / "restart-release"
    original = _queue(workspace, id_generator=lambda: "queue-release")
    item = _add(original, "objective-release", "task-release")
    envelope = _envelope(item)
    volatile = original.claim_pilot(item.queue_item_id, envelope)
    assert isinstance(volatile, bytes) and len(volatile) == 32
    assert "release_capability" not in str(original._stores.queue_db.load())

    restarted = _queue(workspace)
    persisted = restarted.get_pilot_claim(item.queue_item_id)
    assert persisted == {"status": "pilot_claimed", "pilot_attempt": envelope}
    with pytest.raises(ValueError, match="original volatile claim capability"):
        restarted.consume_pilot_send_authority(
            item.queue_item_id, persisted["pilot_attempt"], volatile,
        )
    assert restarted.items()[0].status == "pilot_claimed"

    original.consume_pilot_send_authority(item.queue_item_id, envelope, volatile)
    with pytest.raises(ValueError, match="original volatile claim capability"):
        original.consume_pilot_send_authority(item.queue_item_id, envelope, volatile)
    assert _queue(workspace).items()[0].status == "pilot_unknown"


def test_forged_offline_result_cannot_change_unknown_to_evidence(tmp_path):
    workspace = tmp_path / "forged-offline"
    manager = _queue(workspace, id_generator=lambda: "queue-forged")
    item = _add(manager, "objective-forged", "task-forged")
    manager.claim_pilot(item.queue_item_id, _envelope(item))
    manager.mark_pilot_unknown(item.queue_item_id)

    def forge(records):
        records[0]["status"] = "pilot_evidence_recorded"
        records[0]["result"] = {"outcome": "accepted", "source": "untrusted-offline"}

    with pytest.raises(QueueStoreConflictError, match="evidence|authenticated"):
        manager._stores.queue_db.transact(forge)
    reloaded = _queue(workspace).items()[0]
    assert reloaded.status == "pilot_unknown"
    assert reloaded.result is None
    assert not hasattr(manager, "record_pilot_evidence")


def test_execution_manager_preflight_leaves_objective_unchanged(tmp_path):
    workspace = tmp_path / "executive-guard"
    queue = _queue(workspace, id_generator=lambda: "queue-executive")
    objective = Objective("Synthetic executive objective", objective_id="objective-executive")
    item = _add(queue, objective.objective_id, "task-executive")
    queue.claim_pilot(item.queue_item_id, _envelope(item))

    class Objectives:
        def __init__(self):
            self.calls = []

        def start(self, value):
            self.calls.append("start")
            value.start()

        def complete(self, value):
            self.calls.append("complete")
            value.complete()

        def fail(self, value):
            self.calls.append("fail")
            value.fail()

    objectives = Objectives()
    registry = ExecutionRegistry()
    registry.register("default", ExecutionEngine(queue=queue, planner=object()))
    execution = ExecutionManager(registry=registry, objectives=objectives)

    with pytest.raises(RuntimeError, match="no approved executive lifecycle"):
        execution.execute(objective)
    assert objective.status == "pending"
    assert objective.started is None
    assert objective.completed is None
    assert objectives.calls == []
    assert queue.items()[0].status == "pilot_claimed"
