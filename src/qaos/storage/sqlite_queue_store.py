"""Explicit, local-only transactional queue persistence.

This store is opt-in.  It deliberately has no blind ``save`` operation: queue
mutations must inspect the latest committed records inside ``transact``.  A
SQLite database and a JSON queue are never accepted in the same selected data
directory.  Selecting a backend is not an active-data migration or cutover.

On Windows, the path must be on a fixed local drive, without UNC or reparse
ancestors.  On other platforms, the caller must independently verify that the
selected filesystem is local before deployment; this module cannot certify
every mount implementation.  Tests use isolated temporary directories only.
"""

from __future__ import annotations

import copy
import ctypes
import hashlib
import json
import os
from pathlib import Path
import re
import sqlite3
from typing import Callable, TypeVar


class QueueStoreConflictError(RuntimeError):
    """A queue write would violate canonical identity or attempt authority."""


class QueueStoreDataError(RuntimeError):
    """The selected queue database is invalid or cannot be used safely."""


_T = TypeVar("_T")
_PILOT_STATUSES = frozenset(
    {"pilot_claimed", "pilot_unknown", "pilot_evidence_recorded"}
)
_ALLOWED_PILOT_TRANSITIONS = {
    "pilot_claimed": frozenset(
        {"pilot_claimed", "pilot_unknown", "pilot_evidence_recorded"}
    ),
    "pilot_unknown": frozenset({"pilot_unknown", "pilot_evidence_recorded"}),
    "pilot_evidence_recorded": frozenset({"pilot_evidence_recorded"}),
}
_ATTEMPT_FIELDS = frozenset({
    "queue_item_id", "objective_id", "task_id", "candidate_artifact",
    "acceptance_artifact", "request", "request_sha256", "claimed_at",
})
_REQUEST_FIELDS = frozenset({
    "protocol", "version", "request_id", "nonce", "created_at", "expires_at",
    "objective_id", "task_id", "candidate_artifact", "acceptance_artifact",
    "members", "runtime",
})
_RUNTIME_FIELDS = frozenset({"launcher_sha256", "image_digest", "policy_id"})
_ARTIFACT_FIELDS = frozenset({"artifact_id", "content_sha256"})
_MEMBER_FIELDS = frozenset({"role", "path", "size", "sha256"})
_HEX_SHA256 = re.compile(r"[0-9a-f]{64}\Z")


def _nonempty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value)


def _verify_local_path(path: Path) -> None:
    """Reject known non-local paths and reparse/symlink ancestry.

    A positive Windows check means a fixed drive as reported by the OS; it
    does not approve a future live cutover or substitute for operator review.
    """
    if not path.is_absolute():
        raise QueueStoreDataError("SQLite queue path must be absolute")

    if os.name == "nt":
        anchor = path.anchor
        if not anchor or anchor.startswith("\\\\"):
            raise QueueStoreDataError("SQLite queue requires a local drive")
        # DRIVE_FIXED = 3.  Remote, removable, optical and unknown types fail.
        if ctypes.windll.kernel32.GetDriveTypeW(anchor) != 3:
            raise QueueStoreDataError("SQLite queue requires a fixed local drive")

    for ancestor in (path, *path.parents):
        if ancestor.exists() and (
            ancestor.is_symlink()
            or (hasattr(os.path, "isjunction") and os.path.isjunction(ancestor))
        ):
            raise QueueStoreDataError(
                "SQLite queue path cannot use a symlink or junction"
            )


def _record_id(record: dict) -> str | None:
    value = record.get("queue_item_id")
    if value is None:
        return None
    if not _nonempty_string(value):
        raise QueueStoreConflictError("queue_item_id must be a non-empty string")
    return value


def _attempt_request_id(record: dict) -> str | None:
    attempt = record.get("pilot_attempt")
    if attempt is None:
        return None
    if not isinstance(attempt, dict):
        raise QueueStoreConflictError("pilot_attempt must be an object")
    if set(attempt) != _ATTEMPT_FIELDS:
        raise QueueStoreConflictError("pilot_attempt fields are invalid")
    request = attempt.get("request")
    if not isinstance(request, dict) or set(request) != _REQUEST_FIELDS:
        raise QueueStoreConflictError("frozen pilot request fields are invalid")
    if not _nonempty_string(request.get("request_id")):
        raise QueueStoreConflictError(
            "pilot_attempt requires a frozen request_id"
        )
    if (request.get("protocol") != "qaos.worker.validation"
            or type(request.get("version")) is not int or request["version"] != 1):
        raise QueueStoreConflictError("frozen pilot protocol is invalid")
    for key in ("queue_item_id", "objective_id", "task_id", "claimed_at", "request_sha256"):
        if not _nonempty_string(attempt.get(key)):
            raise QueueStoreConflictError(f"pilot_attempt {key} is invalid")
    if not _HEX_SHA256.fullmatch(attempt["request_sha256"]):
        raise QueueStoreConflictError("pilot request digest is invalid")
    for key in ("objective_id", "task_id", "nonce", "created_at", "expires_at"):
        if not _nonempty_string(request.get(key)):
            raise QueueStoreConflictError(f"frozen pilot {key} is invalid")
    if (
        request["objective_id"] != attempt["objective_id"]
        or request["task_id"] != attempt["task_id"]
    ):
        raise QueueStoreConflictError("pilot request correlation differs from claim")
    for key in ("candidate_artifact", "acceptance_artifact"):
        ref = request.get(key)
        if not isinstance(ref, dict) or set(ref) != _ARTIFACT_FIELDS:
            raise QueueStoreConflictError(f"frozen pilot {key} fields are invalid")
        if not _nonempty_string(ref.get("artifact_id")) or not isinstance(ref.get("content_sha256"), str) or not _HEX_SHA256.fullmatch(ref["content_sha256"]):
            raise QueueStoreConflictError(f"frozen pilot {key} identity is invalid")
        if attempt.get(key) != ref:
            raise QueueStoreConflictError(f"pilot {key} differs from frozen request")
    runtime = request.get("runtime")
    if not isinstance(runtime, dict) or set(runtime) != _RUNTIME_FIELDS or any(
        not _nonempty_string(value) or len(value.encode("utf-8")) > 256
        for value in runtime.values()
    ):
        raise QueueStoreConflictError("frozen pilot runtime fields are invalid")
    members = request.get("members")
    if not isinstance(members, list) or len(members) != 2:
        raise QueueStoreConflictError("frozen pilot member count is invalid")
    for member, role, path, ref in zip(
        members,
        ("acceptance", "candidate"),
        ("acceptance/acceptance.py", "candidate/candidate.py"),
        (request["acceptance_artifact"], request["candidate_artifact"]),
        strict=True,
    ):
        if not isinstance(member, dict) or set(member) != _MEMBER_FIELDS:
            raise QueueStoreConflictError("frozen pilot member fields are invalid")
        if (
            member.get("role") != role or member.get("path") != path
            or type(member.get("size")) is not int
            or not 0 < member["size"] <= 64 * 1024
            or member.get("sha256") != ref["content_sha256"]
        ):
            raise QueueStoreConflictError("frozen pilot member is invalid")
    try:
        request_bytes = json.dumps(
            request, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8", "strict")
    except (TypeError, ValueError, UnicodeError) as error:
        raise QueueStoreConflictError("frozen pilot request cannot be encoded") from error
    if len(request_bytes) > 64 * 1024:
        raise QueueStoreConflictError("frozen pilot request exceeds bounds")
    if hashlib.sha256(request_bytes).hexdigest() != attempt["request_sha256"]:
        raise QueueStoreConflictError("frozen pilot request digest differs from claim")
    return request["request_id"]


def _action_identity(record: dict) -> tuple | None:
    action = record.get("action")
    if action is None:
        return None
    if not isinstance(action, dict):
        raise QueueStoreConflictError("QueueItem action must be an object or null")
    return (action.get("description"), action.get("task_id"), action.get("intent"))


def _validate_records(
    before: list[dict],
    after: list[dict],
    *,
    allow_delete: bool = False,
    fixture_import: bool = False,
) -> None:
    if not isinstance(after, list) or any(not isinstance(row, dict) for row in after):
        raise QueueStoreConflictError("queue records must be a list of objects")

    old_by_id = {
        _record_id(row): row for row in before if _record_id(row) is not None
    }
    new_by_id: dict[str, dict] = {}
    request_ids: set[str] = set()
    origins: dict[tuple[str, str], list[dict]] = {}
    attempted_origins: set[tuple[str, str]] = set()

    for index, row in enumerate(after):
        item_id = _record_id(row)
        if item_id is None:
            if not fixture_import and index >= len(before):
                raise QueueStoreConflictError("new QueueItems require queue_item_id")
        else:
            if item_id in new_by_id:
                raise QueueStoreConflictError("duplicate queue_item_id")
            new_by_id[item_id] = row

        objective_id = row.get("objective_id")
        task_id = row.get("task_id")
        if _nonempty_string(objective_id) and _nonempty_string(task_id):
            pair = (objective_id, task_id)
            origins.setdefault(pair, []).append(row)

        status = row.get("status", "pending")
        if not isinstance(status, str):
            raise QueueStoreConflictError("QueueItem status must be a string")
        request_id = _attempt_request_id(row)
        if request_id is None:
            if status in _PILOT_STATUSES:
                raise QueueStoreConflictError("pilot status requires an attempt")
            continue

        if fixture_import:
            raise QueueStoreConflictError("fixture import cannot import pilot attempts")
        if item_id is None:
            raise QueueStoreConflictError("legacy QueueItem cannot claim a pilot")
        if status not in _PILOT_STATUSES:
            raise QueueStoreConflictError("pilot status cannot regress to an ordinary status")
        if not _nonempty_string(objective_id) or not _nonempty_string(task_id):
            raise QueueStoreConflictError("pilot origin requires Objective and Task IDs")
        action = row.get("action")
        if not isinstance(action, dict) or action.get("task_id") != task_id:
            raise QueueStoreConflictError("pilot origin requires its canonical Task action")
        pair = (objective_id, task_id)
        attempted_origins.add(pair)
        if request_id in request_ids:
            raise QueueStoreConflictError("duplicate pilot request_id")
        request_ids.add(request_id)
        attempt = row["pilot_attempt"]
        if (
            attempt.get("queue_item_id") != item_id
            or attempt.get("objective_id") != objective_id
            or attempt.get("task_id") != task_id
        ):
            raise QueueStoreConflictError("pilot attempt origin does not match QueueItem")
        if status == "pilot_evidence_recorded":
            if row.get("result") is None:
                raise QueueStoreConflictError("recorded pilot evidence requires a result")
        elif row.get("result") is not None:
            raise QueueStoreConflictError("unresolved pilot result must remain empty")

    for pair in attempted_origins:
        if len(origins[pair]) != 1:
            raise QueueStoreConflictError("ambiguous pilot Objective/Task origin")

    if fixture_import:
        return

    # Clear is an explicit all-or-nothing operation.  Allowing a partial
    # deletion here would let a legacy row be replaced or backfilled by index.
    if allow_delete and after:
        raise QueueStoreConflictError("delete transaction must clear the queue")

    # A legacy record cannot be silently backfilled with an ID.  Ordinary
    # transactions retain their existing prefix and only append new records.
    if not allow_delete:
        if len(after) < len(before):
            raise QueueStoreConflictError("queue deletion requires explicit authority")
        for index, old in enumerate(before):
            old_id = _record_id(old)
            new_id = _record_id(after[index])
            if old_id != new_id:
                raise QueueStoreConflictError("QueueItem identity or order changed")
            if old_id is None:
                for key in ("objective", "assignee", "objective_id", "task_id"):
                    if old.get(key) != after[index].get(key):
                        raise QueueStoreConflictError(
                            "legacy QueueItem identity references are immutable"
                        )
                if _action_identity(old) != _action_identity(after[index]):
                    raise QueueStoreConflictError("legacy QueueItem action identity is immutable")

    for old_id, old in old_by_id.items():
        current = new_by_id.get(old_id)
        if current is None:
            if old.get("pilot_attempt") is not None:
                raise QueueStoreConflictError("attempted QueueItem cannot be removed")
            if not allow_delete:
                raise QueueStoreConflictError("QueueItem deletion requires explicit authority")
            continue
        for key in ("objective", "assignee", "objective_id", "task_id"):
            if old.get(key) != current.get(key):
                raise QueueStoreConflictError("QueueItem identity references are immutable")
        if _action_identity(old) != _action_identity(current):
            raise QueueStoreConflictError("QueueItem action identity is immutable")

        old_attempt = old.get("pilot_attempt")
        new_attempt = current.get("pilot_attempt")
        if old_attempt is None and new_attempt is not None:
            if old.get("status", "pending") != "pending" or old.get("result") is not None:
                raise QueueStoreConflictError("pilot claim requires a pending QueueItem")
            if current.get("status") != "pilot_claimed":
                raise QueueStoreConflictError("new pilot claim must be pilot_claimed")
        elif old_attempt is not None:
            if new_attempt != old_attempt:
                raise QueueStoreConflictError("pilot attempt envelope is immutable")
            old_status = old.get("status")
            new_status = current.get("status")
            if new_status == "pilot_evidence_recorded" and old_status != new_status:
                raise QueueStoreConflictError(
                    "authenticated original-stream evidence path is not installed"
                )
            if new_status not in _ALLOWED_PILOT_TRANSITIONS.get(old_status, ()):
                raise QueueStoreConflictError("pilot status cannot regress")
            if old_status == "pilot_evidence_recorded" and old.get("result") != current.get("result"):
                raise QueueStoreConflictError("pilot evidence can be recorded only once")
            for key in ("action", "started", "completed"):
                if old.get(key) != current.get(key):
                    raise QueueStoreConflictError("attempted QueueItem action is frozen")

    for item_id, row in new_by_id.items():
        if item_id not in old_by_id and row.get("pilot_attempt") is not None:
            raise QueueStoreConflictError("pilot claim requires an admitted QueueItem")


class SQLiteQueueStore:
    """Canonical queue store for an explicitly selected fresh local workspace."""

    def __init__(self, path: str | Path):
        self.path = Path(path).absolute()
        if self.path.name != "queue.sqlite3":
            raise ValueError("SQLite queue file must be named queue.sqlite3")
        self._check_path()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._check_path()
        self._initialize()

    def _check_path(self) -> None:
        _verify_local_path(self.path)
        if (self.path.parent / "queue.json").exists():
            raise QueueStoreConflictError(
                "queue.json exists; JSON and SQLite queue authority cannot coexist"
            )

    def _connect(self, *, initialize: bool = False) -> sqlite3.Connection:
        self._check_path()
        connection = sqlite3.connect(self.path, timeout=10, isolation_level=None)
        try:
            connection.execute("PRAGMA busy_timeout=10000")
            journal = connection.execute("PRAGMA journal_mode").fetchone()[0]
            if str(journal).lower() != "wal" and initialize:
                journal = connection.execute("PRAGMA journal_mode=WAL").fetchone()[0]
            if str(journal).lower() != "wal":
                raise QueueStoreDataError("SQLite WAL mode is required")
            connection.execute("PRAGMA synchronous=FULL")
            synchronous = connection.execute("PRAGMA synchronous").fetchone()[0]
            if synchronous != 2:
                raise QueueStoreDataError("SQLite FULL synchronous mode is required")
            return connection
        except Exception:
            connection.close()
            raise

    def _initialize(self) -> None:
        connection = self._connect(initialize=True)
        try:
            connection.execute("BEGIN IMMEDIATE")
            connection.execute(
                "CREATE TABLE IF NOT EXISTS queue_meta ("
                "singleton INTEGER PRIMARY KEY CHECK(singleton = 1), "
                "revision INTEGER NOT NULL CHECK(revision >= 0))"
            )
            connection.execute(
                "INSERT OR IGNORE INTO queue_meta(singleton, revision) VALUES(1, 0)"
            )
            connection.execute(
                "CREATE TABLE IF NOT EXISTS queue_items ("
                "position INTEGER PRIMARY KEY, "
                "queue_item_id TEXT UNIQUE, "
                "objective_id TEXT, task_id TEXT, status TEXT NOT NULL, "
                "pilot_request_id TEXT UNIQUE, record_json TEXT NOT NULL)"
            )
            connection.execute(
                "CREATE INDEX IF NOT EXISTS queue_origin_idx "
                "ON queue_items(objective_id, task_id)"
            )
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    @staticmethod
    def _read(connection: sqlite3.Connection) -> tuple[list[dict], int]:
        meta = connection.execute(
            "SELECT revision FROM queue_meta WHERE singleton = 1"
        ).fetchone()
        if meta is None:
            raise QueueStoreDataError("queue revision metadata is missing")
        records: list[dict] = []
        for position, item_id, objective_id, task_id, status, request_id, payload in connection.execute(
            "SELECT position, queue_item_id, objective_id, task_id, status, "
            "pilot_request_id, record_json FROM queue_items ORDER BY position"
        ):
            if position != len(records):
                raise QueueStoreDataError("queue position sequence is invalid")
            try:
                record = json.loads(payload)
            except (TypeError, ValueError) as error:
                raise QueueStoreDataError("queue record JSON is invalid") from error
            if not isinstance(record, dict):
                raise QueueStoreDataError("queue record must be an object")
            try:
                decoded_id = _record_id(record)
                decoded_request = _attempt_request_id(record)
            except QueueStoreConflictError as error:
                raise QueueStoreDataError("queue record metadata is invalid") from error
            if (
                decoded_id != item_id
                or record.get("objective_id") != objective_id
                or record.get("task_id") != task_id
                or record.get("status", "pending") != status
                or decoded_request != request_id
            ):
                raise QueueStoreDataError("queue record/index metadata differs")
            records.append(record)
        return records, meta[0]

    @staticmethod
    def _write(connection: sqlite3.Connection, records: list[dict], revision: int) -> None:
        connection.execute("DELETE FROM queue_items")
        for index, row in enumerate(records):
            payload = json.dumps(row, ensure_ascii=False, allow_nan=False)
            connection.execute(
                "INSERT INTO queue_items(position, queue_item_id, objective_id, "
                "task_id, status, pilot_request_id, record_json) "
                "VALUES(?, ?, ?, ?, ?, ?, ?)",
                (
                    index,
                    _record_id(row),
                    row.get("objective_id"),
                    row.get("task_id"),
                    row.get("status", "pending"),
                    _attempt_request_id(row),
                    payload,
                ),
            )
        connection.execute(
            "UPDATE queue_meta SET revision = ? WHERE singleton = 1", (revision,)
        )

    def load_with_revision(self) -> tuple[list[dict], int]:
        """Read one committed queue snapshot and its CAS revision."""
        connection = self._connect()
        try:
            connection.execute("BEGIN")
            snapshot = self._read(connection)
            connection.commit()
            return snapshot
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def load(self) -> list[dict]:
        return self.load_with_revision()[0]

    def transact(
        self,
        mutator: Callable[[list[dict]], _T],
        *,
        expected_revision: int | None = None,
        allow_delete: bool = False,
    ) -> _T:
        """Commit a mutation against a fresh, locked queue snapshot.

        ``expected_revision`` fences a manager applying an earlier object
        snapshot.  Selection mutators can instead inspect the fresh records
        they receive and compare the exact selected row before dispatch.
        """
        connection = self._connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            records, revision = self._read(connection)
            if expected_revision is not None and expected_revision != revision:
                raise QueueStoreConflictError("stale queue revision")
            before = copy.deepcopy(records)
            result = mutator(records)
            _validate_records(before, records, allow_delete=allow_delete)
            if records != before:
                self._write(connection, records, revision + 1)
            connection.commit()
            return result
        except sqlite3.IntegrityError as error:
            connection.rollback()
            raise QueueStoreConflictError("queue uniqueness conflict") from error
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def import_legacy_snapshot(self, records: list[dict]) -> None:
        """One-time fixture import into an untouched empty SQLite queue.

        The caller must supply records from a separate test fixture.  This
        method neither reads nor modifies a JSON queue in the selected data
        directory and never backfills missing legacy IDs.
        """
        connection = self._connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            existing, revision = self._read(connection)
            if revision != 0 or existing:
                raise QueueStoreConflictError("fixture import requires a fresh queue")
            imported = copy.deepcopy(records)
            _validate_records([], imported, fixture_import=True)
            self._write(connection, imported, 1)
            connection.commit()
        except sqlite3.IntegrityError as error:
            connection.rollback()
            raise QueueStoreConflictError("fixture import uniqueness conflict") from error
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def save(self, _records: list[dict]) -> None:
        raise QueueStoreConflictError(
            "blind queue save is forbidden; use a fresh SQLite transaction"
        )
