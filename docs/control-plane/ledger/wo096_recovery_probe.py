"""Run with .venv/Scripts/python.exe docs/control-plane/ledger/wo096_recovery_probe.py."""

import hashlib
import json
import tempfile
from pathlib import Path
from unittest.mock import patch

from qaos.application import OperationalSession
from qaos.planner import Task
from qaos.storage import create_stores


def active_fingerprints():
    active = Path(__file__).resolve().parents[3] / "data"
    return {
        path.name: (hashlib.sha256(path.read_bytes()).hexdigest(), path.stat().st_mtime_ns)
        for path in active.glob("*.json")
    }


def state(stores):
    return {
        "objective": [row["status"] for row in stores.objective_db.load()],
        "plan_tasks": [task["status"] for row in stores.plan_db.load()
                       for task in row["tasks"]],
        "queue": [row["status"] for row in stores.queue_db.load()],
        "queue_actions": [row["action"]["status"] for row in stores.queue_db.load()
                          if row.get("action")],
    }


def main():
    before = active_fingerprints()
    evidence = {}
    original_complete = Task.complete
    calls = 0

    def controlled_complete(task):
        nonlocal calls
        calls += 1
        if calls == 2:
            raise RuntimeError("WO-096 controlled second Task failure")
        return original_complete(task)

    with tempfile.TemporaryDirectory(prefix="qaos-wo096-") as workspace:
        stores = create_stores(workspace)
        with patch.object(Task, "complete", controlled_complete):
            try:
                OperationalSession(stores).execute_goal("plan a recovery rehearsal")
            except RuntimeError as error:
                evidence["execution_error"] = str(error)
        evidence["after_failure"] = state(stores)
        objective_id = stores.objective_db.load()[0]["objective_id"]
        try:
            result = OperationalSession(stores).recover_objective(objective_id)
            evidence["recovery_result"] = result.status
        except Exception as error:
            evidence["recovery_error"] = f"{type(error).__name__}: {error}"
        evidence["after_recovery"] = state(stores)
    evidence["temporary_workspace_removed"] = not Path(workspace).exists()
    evidence["active_data_unchanged"] = before == active_fingerprints()
    assert evidence["temporary_workspace_removed"]
    assert evidence["active_data_unchanged"]
    print(json.dumps(evidence, indent=2))


if __name__ == "__main__":
    main()
