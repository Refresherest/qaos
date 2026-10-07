"""Isolated, opt-in queue transaction tests; no active QAOS data is used."""

from __future__ import annotations

import base64
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

from qaos.storage import (
    JSONStore,
    QueueStoreConflictError,
    QueueStoreDataError,
    SQLiteQueueStore,
    create_stores,
)
from qaos.workers.durable_pilot import PILOT_RUNTIME_PINS


def _row(item_id: str, *, objective_id: str = "o1", task_id: str = "t1") -> dict:
    return {
        "objective": "one",
        "objective_id": objective_id,
        "task_id": task_id,
        "assignee": "worker",
        "action": {
            "description": "one", "task_id": task_id, "status": "pending",
            "started": None, "completed": None,
        },
        "queue_item_id": item_id,
        "status": "pending",
        "result": None,
        "started": None,
        "completed": None,
    }


def _attempt(
    row: dict,
    request_id: str = "123e4567-e89b-42d3-a456-426614174000",
) -> dict:
    candidate = {"artifact_id": "candidate", "content_sha256": "a" * 64}
    acceptance = {"artifact_id": "acceptance", "content_sha256": "b" * 64}
    request = {
        "protocol": "qaos.worker.validation", "version": 1,
        "request_id": request_id,
        "nonce": base64.urlsafe_b64encode(b"n" * 32).decode().rstrip("="),
        "created_at": "2026-10-04T00:00:00Z",
        "expires_at": "2026-10-04T00:02:00Z",
        "objective_id": row["objective_id"],
        "task_id": row["task_id"],
        "candidate_artifact": candidate,
        "acceptance_artifact": acceptance,
        "members": [
            {"role": "acceptance", "path": "acceptance/acceptance.py", "size": 1, "sha256": "b" * 64},
            {"role": "candidate", "path": "candidate/candidate.py", "size": 1, "sha256": "a" * 64},
        ],
        "runtime": dict(PILOT_RUNTIME_PINS),
    }
    header = json.dumps(request, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return {
        "queue_item_id": row["queue_item_id"],
        "objective_id": row["objective_id"],
        "task_id": row["task_id"],
        "request": request,
        "candidate_artifact": candidate,
        "acceptance_artifact": acceptance,
        "request_sha256": hashlib.sha256(header).hexdigest(),
        "claimed_at": "2026-10-04T00:00:00Z",
    }


def _claim(records: list[dict], item_id: str = "q1") -> None:
    row = next(row for row in records if row.get("queue_item_id") == item_id)
    row["pilot_attempt"] = _attempt(row)
    row["status"] = "pilot_claimed"


def test_sqlite_is_explicit_opt_in_and_blind_save_refused(tmp_path: Path) -> None:
    default = create_stores(tmp_path / "default")
    assert isinstance(default.queue_db, JSONStore)

    store = create_stores(tmp_path / "sqlite", queue_backend="sqlite").queue_db
    assert isinstance(store, SQLiteQueueStore)
    assert store.path == (tmp_path / "sqlite" / "queue.sqlite3").absolute()
    assert store.load() == []
    assert store.load_with_revision()[1] == 0
    with pytest.raises(QueueStoreConflictError, match="blind queue save"):
        store.save([_row("q1")])
    assert store.load() == []


def test_coexisting_json_queue_is_refused_before_sqlite_creation(tmp_path: Path) -> None:
    data_dir = tmp_path / "collision"
    data_dir.mkdir()
    (data_dir / "queue.json").write_text("[]", encoding="utf-8")
    with pytest.raises(QueueStoreConflictError, match="cannot coexist"):
        create_stores(data_dir, queue_backend="sqlite")
    assert not (data_dir / "queue.sqlite3").exists()


def test_json_created_after_sqlite_selection_blocks_further_access(tmp_path: Path) -> None:
    store = create_stores(tmp_path, queue_backend="sqlite").queue_db
    with pytest.raises(QueueStoreConflictError, match="cannot coexist"):
        create_stores(tmp_path, queue_backend="json")
    (tmp_path / "queue.json").write_text("[]", encoding="utf-8")
    with pytest.raises(QueueStoreConflictError, match="cannot coexist"):
        store.load()


def test_transact_commits_and_rejects_stale_revision(tmp_path: Path) -> None:
    first = create_stores(tmp_path, queue_backend="sqlite").queue_db
    second = create_stores(tmp_path, queue_backend="sqlite").queue_db
    _, old_revision = first.load_with_revision()
    first.transact(lambda records: records.append(_row("q1")), expected_revision=old_revision)
    assert second.load_with_revision() == ([_row("q1")], old_revision + 1)
    with pytest.raises(QueueStoreConflictError, match="stale queue revision"):
        second.transact(
            lambda records: records.append(_row("q2", task_id="t2")),
            expected_revision=old_revision,
        )
    assert [row["queue_item_id"] for row in first.load()] == ["q1"]


def test_two_concurrent_writers_with_same_revision_only_one_commits(tmp_path: Path) -> None:
    store = create_stores(tmp_path, queue_backend="sqlite").queue_db
    _, revision = store.load_with_revision()

    def append(item_id: str) -> str:
        peer = create_stores(tmp_path, queue_backend="sqlite").queue_db
        try:
            peer.transact(
                lambda records: records.append(_row(item_id, task_id=item_id)),
                expected_revision=revision,
            )
            return "committed"
        except QueueStoreConflictError:
            return "stale"

    with ThreadPoolExecutor(max_workers=2) as pool:
        outcomes = list(pool.map(append, ("q1", "q2")))
    assert sorted(outcomes) == ["committed", "stale"]
    assert len(store.load()) == 1


def test_claim_is_immutable_and_pilot_state_monotonic(tmp_path: Path) -> None:
    store = create_stores(tmp_path, queue_backend="sqlite").queue_db
    store.transact(lambda records: records.append(_row("q1")))
    store.transact(_claim)
    claimed = store.load()[0]
    assert claimed["status"] == "pilot_claimed"
    assert claimed["result"] is None

    with pytest.raises(QueueStoreConflictError, match="immutable"):
        store.transact(
            lambda records: records[0]["pilot_attempt"].update(
                claimed_at="2026-10-04T00:00:01Z"
            )
        )
    with pytest.raises(QueueStoreConflictError, match="cannot regress"):
        store.transact(lambda records: records[0].update(status="pending"))
    with pytest.raises(QueueStoreConflictError, match="must remain empty"):
        store.transact(lambda records: records[0].update(result={"premature": True}))

    store.transact(lambda records: records[0].update(status="pilot_unknown"))
    with pytest.raises(QueueStoreConflictError, match="authenticated original-stream"):
        store.transact(
            lambda records: records[0].update(
                status="pilot_evidence_recorded", result={"response_id": "r1"}
            )
        )
    assert store.load()[0]["status"] == "pilot_unknown"
    assert store.load()[0]["result"] is None


def test_attempted_row_cannot_be_deleted_or_aliased(tmp_path: Path) -> None:
    store = create_stores(tmp_path, queue_backend="sqlite").queue_db
    store.transact(lambda records: records.append(_row("q1")))
    store.transact(_claim)

    with pytest.raises(QueueStoreConflictError, match="cannot be removed"):
        store.transact(lambda records: records.clear(), allow_delete=True)
    with pytest.raises(QueueStoreConflictError, match="ambiguous"):
        store.transact(lambda records: records.append(_row("q2")))
    with pytest.raises(QueueStoreConflictError, match="correlation differs"):
        store.transact(
            lambda records: records[0]["pilot_attempt"].update(task_id="other")
        )
    assert len(store.load()) == 1


def test_direct_transaction_rejects_extra_frozen_request_field(tmp_path: Path) -> None:
    store = create_stores(tmp_path, queue_backend="sqlite").queue_db
    store.transact(lambda records: records.append(_row("q1")))

    def unsafe_claim(records):
        attempt = _attempt(records[0])
        attempt["request"]["credential"] = "synthetic-forbidden-field"
        request_bytes = json.dumps(
            attempt["request"], ensure_ascii=False, sort_keys=True,
            separators=(",", ":"),
        ).encode()
        attempt["request_sha256"] = hashlib.sha256(request_bytes).hexdigest()
        records[0]["pilot_attempt"] = attempt
        records[0]["status"] = "pilot_claimed"

    with pytest.raises(QueueStoreConflictError, match="frozen pilot request fields"):
        store.transact(unsafe_claim)
    assert store.load()[0]["status"] == "pending"


def test_claim_refuses_preexisting_ambiguous_pair(tmp_path: Path) -> None:
    store = create_stores(tmp_path, queue_backend="sqlite").queue_db
    store.transact(lambda records: records.extend((_row("q1"), _row("q2"))))
    with pytest.raises(QueueStoreConflictError, match="ambiguous"):
        store.transact(_claim)
    assert all(row.get("pilot_attempt") is None for row in store.load())


def test_duplicate_identity_and_request_id_refused(tmp_path: Path) -> None:
    store = create_stores(tmp_path, queue_backend="sqlite").queue_db
    with pytest.raises(QueueStoreConflictError, match="duplicate queue_item_id"):
        store.transact(lambda records: records.extend((_row("q1"), _row("q1"))))

    store.transact(
        lambda records: records.extend(
            (_row("q1"), _row("q2", objective_id="o2", task_id="t2"))
        )
    )
    store.transact(_claim)

    def duplicate_request(records: list[dict]) -> None:
        row = records[1]
        row["pilot_attempt"] = _attempt(row)
        row["status"] = "pilot_claimed"

    with pytest.raises(QueueStoreConflictError, match="duplicate pilot request_id"):
        store.transact(duplicate_request)


def test_fixture_import_preserves_legacy_rows_without_backfill(tmp_path: Path) -> None:
    store = create_stores(tmp_path, queue_backend="sqlite").queue_db
    legacy = [
        {"objective": "first", "assignee": "a", "status": "completed"},
        {"objective": "second", "assignee": "b", "status": "pending"},
    ]
    store.import_legacy_snapshot(legacy)
    assert store.load() == legacy
    with pytest.raises(QueueStoreConflictError, match="identity or order changed"):
        store.transact(lambda records: records[0].update(queue_item_id="backfill"))
    with pytest.raises(QueueStoreConflictError, match="legacy QueueItem identity"):
        store.transact(lambda records: records[0].update(objective="different"))
    with pytest.raises(QueueStoreConflictError, match="delete transaction must clear"):
        store.transact(lambda records: records.pop(), allow_delete=True)
    store.transact(lambda records: records.append(_row("new")))
    assert [row.get("queue_item_id") for row in store.load()] == [None, None, "new"]
    with pytest.raises(QueueStoreConflictError, match="fresh queue"):
        store.import_legacy_snapshot(legacy)


def test_fixture_import_refuses_attempt_and_is_one_time_even_if_empty(tmp_path: Path) -> None:
    store = create_stores(tmp_path, queue_backend="sqlite").queue_db
    row = _row("q1")
    row["pilot_attempt"] = _attempt(row)
    row["status"] = "pilot_claimed"
    with pytest.raises(QueueStoreConflictError, match="cannot import pilot attempts"):
        store.import_legacy_snapshot([row])
    assert store.load_with_revision() == ([], 0)
    store.import_legacy_snapshot([])
    with pytest.raises(QueueStoreConflictError, match="fresh queue"):
        store.import_legacy_snapshot([])


def test_explicit_all_clear_permits_only_unattempted_rows(tmp_path: Path) -> None:
    store = create_stores(tmp_path, queue_backend="sqlite").queue_db
    store.transact(lambda records: records.extend((_row("q1"), _row("q2", task_id="t2"))))
    store.transact(lambda records: records.clear(), allow_delete=True)
    assert store.load() == []


def test_committed_claim_survives_process_exit(tmp_path: Path) -> None:
    store = create_stores(tmp_path, queue_backend="sqlite").queue_db
    store.transact(lambda records: records.append(_row("q1")))
    attempt = _attempt(_row("q1"))
    script = (
        "import json,sys\n"
        "from qaos.storage import create_stores\n"
        "store=create_stores(sys.argv[1], queue_backend='sqlite').queue_db\n"
        "def claim(records):\n"
        "    row=records[0]\n"
        "    row['pilot_attempt']=json.loads(sys.argv[2])\n"
        "    row['status']='pilot_claimed'\n"
        "store.transact(claim)\n"
    )
    completed = subprocess.run(
        [sys.executable, "-c", script, str(tmp_path), json.dumps(attempt)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr
    assert store.load()[0]["status"] == "pilot_claimed"


@pytest.mark.skipif(os.name != "nt", reason="Windows fixed-drive gate")
def test_windows_unc_queue_path_is_refused() -> None:
    from qaos.storage.sqlite_queue_store import _verify_local_path

    with pytest.raises(QueueStoreDataError, match="local drive"):
        _verify_local_path(Path(r"\\server\share\queue.sqlite3"))


def test_symlinked_queue_parent_is_refused_when_supported(tmp_path: Path) -> None:
    real_parent = tmp_path / "real"
    real_parent.mkdir()
    linked_parent = tmp_path / "link"
    try:
        linked_parent.symlink_to(real_parent, target_is_directory=True)
    except (OSError, NotImplementedError):
        pytest.skip("creating symlinks is not available")
    with pytest.raises(QueueStoreDataError, match="symlink or junction"):
        SQLiteQueueStore(linked_parent / "queue.sqlite3")
