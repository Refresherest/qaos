"""Reproduce the bounded public API rehearsal in fresh Python processes."""

import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[3]


def fingerprint(directory):
    return {str(p.relative_to(directory)): (hashlib.sha256(p.read_bytes()).hexdigest(),
                                           p.stat().st_mtime_ns)
            for p in directory.rglob("*") if p.is_file()}


def child(phase, state, output, identity=None):
    # Suppress normal worker logs; emit only bounded structured evidence.
    with contextlib.redirect_stdout(io.StringIO()):
        from qaos.application import OperationalSession
        from qaos.planner import PythonFileIntent
        from qaos.storage import create_stores

        session = OperationalSession(create_stores(state), python_file_workspace=output)
        if phase == "build":
            objective = session.create_objective("plan public API rehearsal")
            identity = objective.objective_id
        error = None
        try:
            if phase == "build":
                result = session.execute_intent(objective, PythonFileIntent(
                    "built.py", "print('QAOS public API verified')\n",
                    "QAOS public API verified\n",
                ))
                assert result.completed
            elif phase == "recover":
                session.recover_objective(identity)
            else:
                raise ValueError("unknown probe phase")
        except FileExistsError:
            error = "FileExistsError"
    print(json.dumps({"objective_id": identity, "error": error}))
    return 1 if error else 0


def invoke(arguments, expected):
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "src")
    result = subprocess.run([sys.executable, *arguments], cwd=ROOT, env=env,
                            capture_output=True, text=True, timeout=30)
    assert result.returncode == expected, (result.returncode, result.stderr)
    return result.stdout


def records(state, name):
    return json.loads((state / name).read_text(encoding="utf-8"))


def run():
    active_before = fingerprint(ROOT / "data")
    with tempfile.TemporaryDirectory(prefix="qaos-wo121-") as temporary:
        workspace = Path(temporary)
        state, output = workspace / "state", workspace / "output"
        output.mkdir()
        command = [str(Path(__file__).resolve())]
        success = json.loads(invoke(command + ["build", str(state), str(output)], 0))
        first_id = success["objective_id"]
        preserved = {name: records(state, name) for name in
                     ("objectives.json", "plans.json", "queue.json")}
        output_before = fingerprint(output)
        assert (output / "built.py").read_text(encoding="utf-8") == "print('QAOS public API verified')\n"

        before_listing = fingerprint(workspace)
        listing = invoke(["-m", "qaos.main", "objectives", "--workspace", str(state)], 0)
        row = json.loads(listing.splitlines()[1])
        assert row["objective_id"] == first_id and row["status"] == "completed"
        assert fingerprint(workspace) == before_listing

        refused = json.loads(invoke(command + ["build", str(state), str(output)], 1))
        failed_id = refused["objective_id"]
        assert failed_id != first_id and refused["error"] == "FileExistsError"
        recovered = json.loads(invoke(command + ["recover", str(state), str(output), failed_id], 1))
        assert recovered == refused
        objectives = records(state, "objectives.json")
        plans = records(state, "plans.json")
        queue = records(state, "queue.json")
        assert next(row for row in objectives if row["objective_id"] == failed_id)["status"] == "failed"
        failed_plan = next(row for row in plans if row["objective_id"] == failed_id)
        assert failed_plan["tasks"][0]["status"] == "failed"
        failed_items = [row for row in queue if row.get("objective_id") == failed_id and row.get("task_id")]
        assert len(failed_items) == 1
        assert failed_items[0]["status"] == failed_items[0]["action"]["status"] == "failed"
        for name, original in preserved.items():
            current = [row for row in records(state, name) if row.get("objective_id") == first_id]
            assert current == original
        assert fingerprint(output) == output_before

        before_listing = fingerprint(workspace)
        final_listing = invoke(["-m", "qaos.main", "objectives", "--workspace", str(state)], 0)
        statuses = {row["objective_id"]: row["status"] for row in
                    map(json.loads, final_listing.splitlines()[1:])}
        assert statuses == {first_id: "completed", failed_id: "failed"}
        assert fingerprint(workspace) == before_listing
    assert not workspace.exists()
    assert fingerprint(ROOT / "data") == active_before
    print(json.dumps({"exit_codes": [0, 0, 1, 1, 0], "fresh_processes": 5,
                      "public_build": "completed", "collision_and_recovery": "refused",
                      "failure_states_coherent": True, "successful_records_preserved": True,
                      "output_unchanged_after_refusals": True, "listing_read_only": True,
                      "temporary_workspace_removed": True, "active_data_unchanged": True}, indent=2))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        sys.exit(child(*sys.argv[1:]))
    run()
