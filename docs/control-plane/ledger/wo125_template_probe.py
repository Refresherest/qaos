"""Bounded fresh-process rehearsal of the approved trusted-template contract."""

import contextlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile

from wo121_public_api_probe import ROOT, fingerprint, invoke, records


def child(phase, state, output, identity=None):
    if phase == "import":
        sys.dont_write_bytecode = True
        captured = io.StringIO()
        with contextlib.redirect_stdout(captured), contextlib.redirect_stderr(captured):
            spec = importlib.util.spec_from_file_location("generated_stats", Path(output) / "stats.py")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            assert module.text_stats("one two\nthree") == {"characters": 13, "words": 3, "lines": 2}
            assert module.text_stats("猫 café") == {"characters": 6, "words": 2, "lines": 1}
            try:
                module.text_stats(None)
            except TypeError:
                pass
            else:
                raise AssertionError("non-string accepted")
        assert captured.getvalue() == ""
        print(json.dumps({"import_and_use": "passed"}))
        return 0

    with contextlib.redirect_stdout(io.StringIO()):
        from qaos.application import OperationalSession
        from qaos.planner import PythonTemplateIntent
        from qaos.storage import create_stores

        options = {"python_file_workspace": Path(output)}
        if phase == "build":
            options["enabled_python_templates"] = ("text_stats_v1",)
        elif phase == "recover_default":
            options = {}
        elif phase != "recover_file_only":
            raise ValueError("unknown phase")
        session = OperationalSession(create_stores(Path(state)), **options)
        error = None
        try:
            if phase == "build":
                objective = session.create_objective("plan trusted template rehearsal")
                identity = objective.objective_id
                assert session.execute_intent(objective, PythonTemplateIntent("stats.py")).completed
            else:
                session.recover_objective(identity)
                raise AssertionError("disabled recovery accepted")
        except FileExistsError:
            assert phase == "build"
            error = "FileExistsError"
        except ValueError as exc:
            assert phase.startswith("recover") and str(exc) == "template is not enabled"
            error = str(exc)
    print(json.dumps({"objective_id": identity, "error": error}))
    return 1 if error else 0


def run():
    active_before = fingerprint(ROOT / "data")
    with tempfile.TemporaryDirectory(prefix="qaos-wo125-") as temporary:
        workspace = Path(temporary)
        state, output = workspace / "state", workspace / "output"
        output.mkdir()
        command = [str(Path(__file__).resolve())]
        def phase(name, expected=0, identity=None):
            arguments = command + [name, str(state), str(output)]
            if identity:
                arguments.append(identity)
            return json.loads(invoke(arguments, expected))

        first = phase("build")
        first_id = first["objective_id"]
        preserved = {name: records(state, name) for name in
                     ("objectives.json", "plans.json", "queue.json")}
        before = fingerprint(workspace)
        assert phase("import") == {"import_and_use": "passed"}
        assert fingerprint(workspace) == before
        listing = invoke(["-m", "qaos.main", "objectives", "--workspace", str(state)], 0)
        row = json.loads(listing.splitlines()[1])
        assert row["objective_id"] == first_id and row["status"] == "completed"
        assert fingerprint(workspace) == before
        output_before = fingerprint(output)

        failed = phase("build", 1)
        failed_id = failed["objective_id"]
        assert failed_id != first_id and failed["error"] == "FileExistsError"
        before_denial = fingerprint(workspace)
        for mode in ("recover_file_only", "recover_default"):
            assert phase(mode, 1, failed_id) == {
                "objective_id": failed_id, "error": "template is not enabled"}
            assert fingerprint(workspace) == before_denial
        assert next(r for r in records(state, "objectives.json")
                    if r["objective_id"] == failed_id)["status"] == "failed"
        plan = next(r for r in records(state, "plans.json") if r["objective_id"] == failed_id)
        assert plan["tasks"][0]["status"] == "failed"
        items = [r for r in records(state, "queue.json")
                 if r.get("objective_id") == failed_id and r.get("task_id")]
        assert len(items) == 1 and items[0]["status"] == items[0]["action"]["status"] == "failed"
        for name, original in preserved.items():
            assert [r for r in records(state, name) if r.get("objective_id") == first_id] == original
        assert fingerprint(output) == output_before
    assert not workspace.exists()
    assert fingerprint(ROOT / "data") == active_before
    print(json.dumps({"fresh_processes": 6, "exit_codes": [0, 0, 0, 1, 1, 1],
                      "build_import_discovery": "passed", "collision": "refused",
                      "disabled_recovery_modes": 2, "denials_read_only": True,
                      "failure_states_coherent": True, "successful_records_preserved": True,
                      "output_preserved": True, "temporary_workspace_removed": True,
                      "active_data_unchanged": True}, indent=2))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        sys.exit(child(*sys.argv[1:]))
    run()
