"""Tests for explicit queue-worker composition."""

from __future__ import annotations

import qaos.queue.manager as manager_module
from qaos.queue import QueueItem, QueueManager
from qaos.storage import create_stores


def test_explicit_queue_uses_selected_worker_service(tmp_path) -> None:
    stores = create_stores(tmp_path / "queue")
    calls = []

    class Worker:
        def execute(self, item):
            calls.append(item)
            item.status = "completed"
            item.result = "selected worker"

    class Workers:
        def get(self, name):
            assert name == "default"
            return Worker()

    manager = QueueManager(stores=stores, workers=Workers())
    item = QueueItem("isolated queue objective", "selected assignee")
    manager.add(item)

    manager.process()

    assert calls == [item]
    assert item.status == "completed"
    assert item.result == "selected worker"
    assert stores.queue_db.load()[0]["result"] == "selected worker"


def test_queue_default_constructor_retains_default_worker_service(
    monkeypatch, tmp_path
) -> None:
    default_workers = object()
    monkeypatch.setattr(manager_module, "worker_manager", default_workers)

    manager = QueueManager(stores=create_stores(tmp_path / "default-workers"))

    assert manager._workers is default_workers
