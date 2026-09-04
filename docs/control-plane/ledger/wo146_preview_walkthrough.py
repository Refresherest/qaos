"""Disposable public-command preview/refusal and separately authorized build."""
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
    with tempfile.TemporaryDirectory(prefix=".wo146-preview-", dir=ROOT) as temporary:
        root = Path(temporary).resolve()
        assert root.parent == ROOT.resolve()
        state, output = root / "state", root / "output"
        state.mkdir()
        output.mkdir()
        def invoke(name, args, expected):
            env = os.environ.copy()
            env["PYTHONPATH"] = str(ROOT / "src")
            result = subprocess.run([sys.executable, "-B", *args], cwd=root, env=env,
                                    capture_output=True, text=True, timeout=110, shell=False)
            assert result.returncode == expected, (name, result.stderr)
            phases.append({"phase": name, "exit_code": result.returncode})
            return result
        preview_args = ["-m", "qaos.main", "preview-project", "--directory", "Example", "--brief"]
        before = fingerprint(root)
        previews = []
        for name, brief in (("preview", "count words and lines"),
                            ("normalized_preview", "  Count LINES  and words  ")):
            result = invoke(name, [*preview_args, brief], 0)
            assert not result.stderr and len(result.stdout.splitlines()) == 1
            previews.append(json.loads(result.stdout))
        expected = {"status": "preview", "grammar_version": 1, "intent": {
            "type": "python_project", "version": 2, "template_id": "text_stats_project_v2",
            "relative_directory": "Example", "metrics": ["words", "lines"]}}
        assert previews == [expected, expected]
        errors = []
        for name, args in (("unsupported_clause", [*preview_args, "count words and publish it"]),
                           ("duplicate_metric", [*preview_args, "count words and words"]),
                           ("preview_permission_flag", [*preview_args, "count words", "--enable-project", "text_stats_project_v2"])):
            result = invoke(name, args, 2)
            assert not result.stdout and "Grammar:" in result.stderr
            errors.append(result.stderr)
        assert len(set(errors)) == 1
        assert fingerprint(root) == before and not list(state.iterdir()) and not list(output.iterdir())
        assert {p.name for p in root.iterdir()} == {"state", "output"}
        build = ["-m", "qaos.main", "build-project", "--workspace", str(state),
                 "--output-root", str(output), "--directory", "Example", "--metrics", "words,lines"]
        denied = invoke("build_without_permission", build, 2)
        assert "Objective ID:" not in denied.stdout and fingerprint(root) == before
        build += ["--enable-project", "text_stats_project_v2"]
        result = invoke("separate_authorized_build", build, 0)
        assert "Status: completed" in result.stdout
        saved = {name: records(state, name) for name in ("objectives.json", "plans.json", "queue.json")}
        assert saved["plans.json"][0]["tasks"][0]["intent"] == expected["intent"]
        identity = saved["objectives.json"][0]["objective_id"]
        assert f"Objective ID: {identity}" in result.stdout
        published = fingerprint(output)
        before = fingerprint(root)
        app = invoke("standalone_use", ["-E", "-s", str(output / "Example" / "app.py"), "--text", "one two\nthree"], 0)
        assert json.loads(app.stdout) == {"words": 3, "lines": 2} and not app.stderr
        listing = invoke("discovery", ["-m", "qaos.main", "objectives", "--workspace", str(state)], 0)
        assert identity in listing.stdout and "completed" in listing.stdout
        assert fingerprint(root) == before
        collision = invoke("collision", build, 1)
        assert "FileExistsError" in collision.stderr
        for name, original in saved.items():
            assert [r for r in records(state, name) if r.get("objective_id") == identity] == original
        assert fingerprint(output) == published and {p.name for p in output.iterdir()} == {"Example"}
        assert root.parent == ROOT.resolve() and not root.is_symlink()
    assert not root.exists() and fingerprint(ROOT / "data") == active
    print(json.dumps({"phases": phases, "preview_and_refusals_no_writes": True,
                      "separate_build_matches_preview": True, "successful_output_preserved": True,
                      "active_data_unchanged": True, "temporary_workspace_removed": True}, indent=2))


if __name__ == "__main__":
    run()
