"""Fresh-process CLI build/use/discovery and authorization rehearsal."""

import contextlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile

from wo121_public_api_probe import ROOT, fingerprint, invoke, records


def child(mode, state, output, identity=None):
    with contextlib.redirect_stdout(io.StringIO()):
        from qaos.application import OperationalSession
        from qaos.planner import PythonTemplateIntent
        from qaos.storage import create_stores
        options = {"python_file_workspace": Path(output)}
        if mode == "build":
            options["enabled_python_templates"] = ("text_stats_cli_v1",)
        elif mode == "default":
            options = {}
        elif mode == "old_template":
            options["enabled_python_templates"] = ("text_stats_v1",)
        elif mode != "file_only":
            raise ValueError("unknown probe mode")
        session = OperationalSession(create_stores(Path(state)), **options)
        error = None
        try:
            if mode == "build":
                obj = session.create_objective("plan CLI rehearsal")
                identity = obj.objective_id
                assert session.execute_intent(obj, PythonTemplateIntent(
                    "app.py", template_id="text_stats_cli_v1")).completed
            else:
                session.recover_objective(identity)
                raise AssertionError("disabled recovery accepted")
        except FileExistsError:
            assert mode == "build"
            error = "FileExistsError"
        except ValueError as exc:
            assert mode != "build" and str(exc) == "template is not enabled"
            error = str(exc)
    print(json.dumps({"objective_id": identity, "error": error}))
    return 1 if error else 0


def run():
    active_before = fingerprint(ROOT / "data")
    with tempfile.TemporaryDirectory(prefix="qaos-wo129-") as temporary:
        root = Path(temporary)
        state, output = root / "state", root / "output"
        output.mkdir()
        def phase(mode, expected=0, identity=None):
            args = [str(Path(__file__).resolve()), mode, str(state), str(output)]
            return json.loads(invoke(args + ([identity] if identity else []), expected))
        first = phase("build")["objective_id"]
        saved = {name: records(state, name) for name in
                 ("objectives.json", "plans.json", "queue.json")}
        task = next(r for r in saved["queue.json"] if r.get("task_id"))
        assert task["result"]["cli_cases_passed"] == 15
        before = fingerprint(root)
        for arguments, code, expected in (
            (["--text", "one two\nthree"], 0, {"characters": 13, "words": 3, "lines": 2}),
            (["--unknown"], 2, None),
        ):
            result = subprocess.run([sys.executable, "-I", str(output / "app.py"), *arguments],
                                    cwd=output, capture_output=True, text=True,
                                    timeout=5, shell=False)
            assert result.returncode == code
            if expected is None:
                assert result.stdout == "" and result.stderr == "Invalid text arguments\n"
            else:
                assert json.loads(result.stdout) == expected and result.stderr == ""
            assert fingerprint(root) == before
        listing = invoke(["-m", "qaos.main", "objectives", "--workspace", str(state)], 0)
        row = json.loads(listing.splitlines()[1])
        assert row["objective_id"] == first and row["status"] == "completed"
        assert fingerprint(root) == before
        output_before = fingerprint(output)
        failed = phase("build", 1)
        identity = failed["objective_id"]
        assert identity != first and failed["error"] == "FileExistsError"
        before_denial = fingerprint(root)
        for mode in ("default", "file_only", "old_template"):
            assert phase(mode, 1, identity)["error"] == "template is not enabled"
            assert fingerprint(root) == before_denial
        for name, original in saved.items():
            assert [r for r in records(state, name) if r.get("objective_id") == first] == original
        assert next(r for r in records(state, "objectives.json")
                    if r["objective_id"] == identity)["status"] == "failed"
        assert next(r for r in records(state, "plans.json")
                    if r["objective_id"] == identity)["tasks"][0]["status"] == "failed"
        item = next(r for r in records(state, "queue.json")
                    if r.get("objective_id") == identity and r.get("task_id"))
        assert item["status"] == item["action"]["status"] == "failed"
        assert fingerprint(output) == output_before
    assert not root.exists() and fingerprint(ROOT / "data") == active_before
    print(json.dumps({"fresh_top_level_processes": 8, "exit_codes": [0, 0, 2, 0, 1, 1, 1, 1],
                      "build_cli_discovery": "passed", "disabled_recovery_modes": 3,
                      "read_only_checks": "passed", "failure_states": "coherent",
                      "successful_records_and_output": "preserved",
                      "temporary_workspace_removed": True, "active_data_unchanged": True}, indent=2))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        sys.exit(child(*sys.argv[1:]))
    run()
