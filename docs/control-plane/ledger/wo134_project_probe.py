"""Bounded project rehearsal across fresh processes on local Windows/NTFS."""
import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

from wo121_public_api_probe import ROOT, fingerprint, records


def child(mode, state, output, identity=None):
    with contextlib.redirect_stdout(io.StringIO()):
        from qaos.application import OperationalSession
        from qaos.planner import PythonProjectIntent
        from qaos.storage import create_stores
        options = {}
        if mode in ("build", "recover"):
            options = {"python_project_workspace": Path(output),
                       "enabled_python_projects": ("text_stats_project_v1",)}
        elif mode == "old_template":
            options = {"python_file_workspace": Path(output),
                       "enabled_python_templates": ("text_stats_cli_v1",)}
        elif mode == "project_root_only":
            options = {"python_project_workspace": Path(output)}
        elif mode != "default":
            raise ValueError("unknown phase")
        session = OperationalSession(create_stores(Path(state)), **options)
        error = None
        try:
            if mode == "build":
                obj = session.create_objective("plan project rehearsal")
                identity = obj.objective_id
                assert session.execute_intent(obj, PythonProjectIntent("Example")).completed
            else:
                session.recover_objective(identity)
                raise AssertionError("unexpected recovery success")
        except FileExistsError:
            assert mode in ("build", "recover")
            error = "FileExistsError"
        except ValueError as exc:
            assert mode not in ("build", "recover") and str(exc) == "project template is not enabled"
            error = str(exc)
    print(json.dumps({"objective_id": identity, "error": error}))
    return 1 if error else 0


def run():
    active_before = fingerprint(ROOT / "data")
    with tempfile.TemporaryDirectory(prefix=".wo134-probe-", dir=ROOT) as temporary:
        root = Path(temporary).resolve()
        assert root.parent == ROOT.resolve()
        state, output = root / "state", root / "output"
        output.mkdir()
        codes = []
        def invoke(args, expected, cwd=ROOT):
            env = os.environ.copy()
            env["PYTHONPATH"] = str(ROOT / "src")
            result = subprocess.run([sys.executable, *args], cwd=cwd, env=env,
                                    capture_output=True, text=True, timeout=110, shell=False)
            codes.append(result.returncode)
            assert result.returncode == expected, result.stderr
            return result.stdout
        def phase(mode, code=0, identity=None):
            args = [str(Path(__file__).resolve()), mode, str(state), str(output)]
            return json.loads(invoke(args + ([identity] if identity else []), code))
        first = phase("build")["objective_id"]
        saved = {name: records(state, name) for name in ("objectives.json", "plans.json", "queue.json")}
        project = output / "Example"
        assert {p.name for p in project.iterdir()} == {"stats.py", "app.py", "test_stats.py", "README.md"}
        evidence = next(r["result"] for r in saved["queue.json"] if r.get("task_id"))
        assert evidence["published"] and evidence["cli_cases_passed"] == 15
        assert evidence["member_sha256"] == {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                             for p in project.iterdir()}
        before = fingerprint(root)
        app = invoke(["-E", "-s", "-B", str(project / "app.py"), "--text", "one two\nthree"], 0, project)
        assert json.loads(app) == {"characters": 13, "words": 3, "lines": 2}
        tests = invoke(["-E", "-s", "-B", str(project / "test_stats.py")], 0, project)
        assert tests == "QAOS project tests PASS\n"
        listing = invoke(["-m", "qaos.main", "objectives", "--workspace", str(state)], 0)
        row = json.loads(listing.splitlines()[1])
        assert row["objective_id"] == first and row["status"] == "completed"
        assert fingerprint(root) == before
        output_before = fingerprint(output)
        failed = phase("build", 1)
        identity = failed["objective_id"]
        assert identity != first and failed["error"] == "FileExistsError"
        for mode in ("default", "old_template", "project_root_only"):
            before = fingerprint(root)
            assert phase(mode, 1, identity)["error"] == "project template is not enabled"
            assert fingerprint(root) == before
        assert phase("recover", 1, identity)["error"] == "FileExistsError"
        for name, original in saved.items():
            assert [r for r in records(state, name) if r.get("objective_id") == first] == original
        assert next(r for r in records(state, "objectives.json") if r["objective_id"] == identity)["status"] == "failed"
        assert next(r for r in records(state, "plans.json") if r["objective_id"] == identity)["tasks"][0]["status"] == "failed"
        item = next(r for r in records(state, "queue.json") if r.get("objective_id") == identity and r.get("task_id"))
        assert item["status"] == item["action"]["status"] == "failed"
        assert fingerprint(output) == output_before and {p.name for p in output.iterdir()} == {"Example"}
        assert root.parent == ROOT.resolve() and not root.is_symlink()
    assert not root.exists() and fingerprint(ROOT / "data") == active_before
    print(json.dumps({"fresh_top_level_processes": len(codes), "exit_codes": codes,
                      "four_file_build_use_discovery": "passed", "disabled_recovery_modes": 3,
                      "authorized_existing_output_recovery": "refused", "failed_states": "coherent",
                      "successful_records_and_output_preserved": True, "denials_read_only": True,
                      "temporary_workspace_removed": True, "active_data_unchanged": True}, indent=2))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        sys.exit(child(*sys.argv[1:]))
    run()
