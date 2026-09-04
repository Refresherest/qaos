"""Run the shipped CLI with disposable roots; no product feature changes."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

from wo121_public_api_probe import ROOT, fingerprint, records


def run():
    active = fingerprint(ROOT / "data")
    phases = []
    with tempfile.TemporaryDirectory(prefix=".wo142-walkthrough-", dir=ROOT) as temporary:
        root = Path(temporary).resolve()
        assert root.parent == ROOT.resolve()
        state, output = root / "state", root / "output"
        state.mkdir()
        output.mkdir()
        args = ["-m", "qaos.main", "build-project", "--workspace", str(state),
                "--output-root", str(output), "--directory", "Example",
                "--metrics", "lines,words", "--enable-project", "text_stats_project_v2"]
        def invoke(name, command, expected):
            env = os.environ.copy()
            env["PYTHONPATH"] = str(ROOT / "src")
            result = subprocess.run([sys.executable, *command], cwd=root, env=env,
                                    capture_output=True, text=True, timeout=110, shell=False)
            assert result.returncode == expected, (name, result.returncode, result.stderr)
            phases.append({"phase": name, "exit_code": result.returncode})
            return result
        def denial(name, command, expected, error):
            before = fingerprint(root)
            result = invoke(name, command, expected)
            assert error in result.stderr and "Objective ID:" not in result.stdout
            assert fingerprint(root) == before
        denial("missing_permission", args[:-2], 2, "Usage:")
        missing = args.copy()
        missing[4] = str(root / "missing")
        denial("missing_state_root", missing, 1, "Project build failed (ValueError).")
        assert not (root / "missing").exists()
        overlap = args.copy()
        overlap[6] = str(state)
        denial("overlapping_roots", overlap, 1, "Project build failed (ValueError).")
        result = invoke("build", args, 0)
        assert "Status: completed" in result.stdout and "Metrics: words,lines" in result.stdout
        saved = {name: records(state, name) for name in ("objectives.json", "plans.json", "queue.json")}
        identity = saved["objectives.json"][0]["objective_id"]
        assert f"Objective ID: {identity}" in result.stdout
        project = output / "Example"
        assert {p.name for p in project.iterdir()} == {"stats.py", "app.py", "test_stats.py", "README.md"}
        evidence = next(r["result"] for r in saved["queue.json"] if r.get("task_id"))
        assert evidence["metrics"] == ["words", "lines"] and evidence["published"]
        assert evidence["member_sha256"] == {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in project.iterdir()}
        before = fingerprint(root)
        app = invoke("standalone_use", ["-E", "-s", "-B", str(project / "app.py"), "--text", "one two\nthree"], 0)
        assert json.loads(app.stdout) == {"words": 3, "lines": 2} and not app.stderr
        tests = invoke("generated_tests", ["-E", "-s", "-B", str(project / "test_stats.py")], 0)
        assert tests.stdout == "QAOS project tests PASS\n" and not tests.stderr
        listing = invoke("discovery", ["-m", "qaos.main", "objectives", "--workspace", str(state)], 0)
        assert identity in listing.stdout and "completed" in listing.stdout
        assert fingerprint(root) == before
        published = fingerprint(output)
        collision = invoke("collision", args, 1)
        assert "Project build failed (FileExistsError)." in collision.stderr
        failed = next(r for r in records(state, "objectives.json") if r["objective_id"] != identity)
        assert failed["status"] == "failed" and f"Objective ID: {failed['objective_id']}" in collision.stdout
        plan = next(r for r in records(state, "plans.json") if r["objective_id"] == failed["objective_id"])
        assert plan["tasks"][0]["status"] == "failed"
        item = next(r for r in records(state, "queue.json") if r.get("task_id") and r["objective_id"] == failed["objective_id"])
        assert item["status"] == item["action"]["status"] == "failed"
        before = fingerprint(root)
        recovery = invoke("default_recovery", ["-m", "qaos.main", "recover", "--workspace", str(state), failed["objective_id"]], 1)
        assert "Objective recovery failed (ValueError)." in recovery.stderr
        assert fingerprint(root) == before
        for name, original in saved.items():
            assert [r for r in records(state, name) if r.get("objective_id") == identity] == original
        assert fingerprint(output) == published and {p.name for p in output.iterdir()} == {"Example"}
        assert root.parent == ROOT.resolve() and not root.is_symlink()
    assert not root.exists() and fingerprint(ROOT / "data") == active
    print(json.dumps({"phases": phases, "normalized_metrics": ["words", "lines"],
                      "standalone_output": {"words": 3, "lines": 2},
                      "early_refusals_read_only": True, "successful_build_preserved": True,
                      "failed_state_coherent": True, "active_data_unchanged": True,
                      "disposable_workspace_removed": True}, indent=2))


if __name__ == "__main__":
    run()
