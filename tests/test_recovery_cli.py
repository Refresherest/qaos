"""OWNER-DECISION-018 command contract and real subprocess recovery."""

import os
from pathlib import Path
import subprocess
import sys
from unittest.mock import patch

import pytest

from qaos.application import OperationalSession
from qaos.main import main
from qaos.objectives import Objective
from qaos.planner import Task
from qaos.storage import create_stores


@pytest.mark.parametrize("args", [[], ["--workspace"], ["--workspace", "x"],
    ["--workspace", "x", "id", "extra"], ["--other", "x", "id"],
    ["--workspace", " ", "id"], ["--workspace", "x", " "]])
def test_invalid_usage_never_constructs_session(args, monkeypatch, capsys):
    def forbidden(*args):
        pytest.fail("must validate before session construction")
    monkeypatch.setattr("qaos.commands.recover.OperationalSession", forbidden)
    assert main(["recover", *args]) == 2
    assert "Usage:" in capsys.readouterr().err


def test_missing_workspace_is_not_created(tmp_path, capsys):
    missing = tmp_path / "missing"
    assert main(["recover", "--workspace", str(missing), "id"]) == 1
    assert not missing.exists()
    assert "Traceback" not in capsys.readouterr().err


@pytest.mark.parametrize("status,expected", [("completed", 0), ("failed", 1)])
def test_exact_id_single_call_and_canonical_status(tmp_path, monkeypatch, capsys,
                                                  status, expected):
    calls = []
    objective = Objective("test", objective_id=" id ")
    objective.status = status
    objective.completed = "timestamp-is-not-a-success-flag"

    class Session:
        def __init__(self, stores):
            pass

        def recover_objective(self, value):
            calls.append(value)
            return objective

    monkeypatch.setattr("qaos.commands.recover.OperationalSession", Session)
    assert main(["recover", "--workspace", str(tmp_path), " id "]) == expected
    assert calls == [" id "]
    output = capsys.readouterr()
    assert ("Status: completed" in output.out) == (expected == 0)


def test_exception_payload_is_not_exposed(tmp_path, monkeypatch, capsys):
    def fail(*args):
        raise RuntimeError("sensitive-test-payload")
    monkeypatch.setattr("qaos.commands.recover.execute", fail)
    assert main(["recover", "--workspace", str(tmp_path), "id"]) == 1
    output = capsys.readouterr()
    assert "sensitive-test-payload" not in output.err + output.out
    assert "RuntimeError" in output.err


def test_actual_failure_then_subprocess_cli_recovery(tmp_path):
    stores = create_stores(tmp_path)
    original = Task.complete
    calls = 0

    def fail_second(task):
        nonlocal calls
        calls += 1
        if calls == 2:
            raise RuntimeError("controlled CLI rehearsal failure")
        return original(task)

    with patch.object(Task, "complete", fail_second):
        with pytest.raises(RuntimeError):
            OperationalSession(stores).execute_goal("plan CLI recovery")
    objective_id = stores.objective_db.load()[0]["objective_id"]
    completed_task = stores.plan_db.load()[0]["tasks"][0]
    root = Path(__file__).resolve().parents[1]
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(root / "src")
    result = subprocess.run(
        [sys.executable, "-m", "qaos.main", "recover", "--workspace",
         str(tmp_path), objective_id], cwd=root, env=environment,
        capture_output=True, text=True, timeout=30,
    )
    assert result.returncode == 0, result.stderr
    assert f"Objective ID: {objective_id}" in result.stdout
    assert "Status: completed" in result.stdout
    assert stores.plan_db.load()[0]["tasks"][0] == completed_task
    assert all(row["status"] == "completed" for row in stores.queue_db.load())
    assert stores.objective_db.load()[0]["status"] == "completed"
