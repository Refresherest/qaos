"""Reproduce the bounded full operator flow without changing product code."""
import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from unittest.mock import patch

from qaos.main import main
from qaos.planner import Task
from qaos.storage import create_stores

ROOT = Path(__file__).resolve().parents[3]


def fingerprint(directory):
    return {str(p.relative_to(directory)): (hashlib.sha256(p.read_bytes()).hexdigest(),
                                           p.stat().st_mtime_ns)
            for p in directory.rglob("*") if p.is_file()}


def cli(*args):
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "src")
    return subprocess.run([sys.executable, "-m", "qaos.main", *args],
                          cwd=ROOT, env=env, capture_output=True, text=True, timeout=30)


def run():
    active_before = fingerprint(ROOT / "data")
    evidence = {}
    with tempfile.TemporaryDirectory(prefix="qaos-wo107-") as workspace:
        stores = create_stores(workspace)
        original = Task.complete
        count = 0
        def fail_second(task):
            nonlocal count
            count += 1
            if count == 2:
                raise RuntimeError("controlled private failure text")
            return original(task)
        output, errors = io.StringIO(), io.StringIO()
        with patch.object(Task, "complete", fail_second), \
                contextlib.redirect_stdout(output), contextlib.redirect_stderr(errors):
            code = main(["objective", "--workspace", workspace, "plan operator rehearsal"])
        identity = output.getvalue().splitlines()[0].removeprefix("Objective ID: ")
        assert code == 1 and identity == stores.objective_db.load()[0]["objective_id"]
        assert "controlled private" not in output.getvalue() + errors.getvalue()
        completed_task = stores.plan_db.load()[0]["tasks"][0]
        before_listing = fingerprint(Path(workspace))
        discovery = cli("objectives", "--workspace", workspace)
        assert discovery.returncode == 0
        row = json.loads(discovery.stdout.splitlines()[1])
        assert row["objective_id"] == identity and row["status"] == "failed"
        assert before_listing == fingerprint(Path(workspace))
        recovery = cli("recover", "--workspace", workspace, identity)
        assert recovery.returncode == 0, recovery.stderr
        assert completed_task == stores.plan_db.load()[0]["tasks"][0]
        assert all(row["status"] == "completed" for row in stores.queue_db.load())
        before_listing = fingerprint(Path(workspace))
        rediscovery = cli("objectives", "--workspace", workspace)
        assert rediscovery.returncode == 0
        row = json.loads(rediscovery.stdout.splitlines()[1])
        assert row["objective_id"] == identity and row["status"] == "completed"
        assert before_listing == fingerprint(Path(workspace))
        evidence.update(exit_codes=[code, discovery.returncode, recovery.returncode,
                                    rediscovery.returncode], identity_consistent=True,
                        discovered_status="failed", rediscovered_status="completed",
                        completed_task_preserved=True, listings_read_only=True)
    assert not Path(workspace).exists()
    assert active_before == fingerprint(ROOT / "data")
    evidence.update(temporary_workspace_removed=True, active_data_unchanged=True)
    print(json.dumps(evidence, indent=2))


if __name__ == "__main__":
    run()
