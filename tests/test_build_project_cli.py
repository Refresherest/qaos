import itertools
import json
import os
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace

import pytest
from qaos.commands import build_project as command
from qaos.main import main


def arguments(state, output, metrics="lines,words"):
    return ["--workspace", str(state), "--output-root", str(output),
            "--directory", "Example", "--metrics", metrics,
            "--enable-project", "text_stats_project_v2"]


def snapshot(root):
    return {str(p.relative_to(root)): (p.read_bytes(), p.stat().st_mtime_ns)
            for p in root.rglob("*") if p.is_file()}


@pytest.mark.parametrize("index", range(5))
@pytest.mark.parametrize("mutation", ["missing", "duplicate", "unknown", "blank"])
def test_bad_options_never_touch_stores(index, mutation, monkeypatch):
    args = arguments("state", "output")
    offset = index * 2
    if mutation == "missing":
        del args[offset:offset + 2]
    elif mutation == "duplicate":
        args += args[offset:offset + 2]
    elif mutation == "unknown":
        args[offset] += "x"
    else:
        args[offset + 1] = " "
    monkeypatch.setattr(command, "create_stores", lambda *_: pytest.fail("store accessed"))
    assert main(["build-project", *args]) == 2


@pytest.mark.parametrize("value", ["words,", ",words", "words,words", "Words", " words", "words, lines", "unknown"])
def test_bad_metrics(value, monkeypatch):
    monkeypatch.setattr(command, "validate_roots", lambda *_: pytest.fail("roots accessed"))
    assert command.execute(arguments("state", "output", value)) == 2


def test_permission_and_extra_values(monkeypatch):
    monkeypatch.setattr(command, "validate_roots", lambda *_: pytest.fail("roots accessed"))
    args = arguments("state", "output")
    assert command.execute(args + ["extra"]) == 2
    args[-1] = "text_stats_project_v1"
    assert command.execute(args) == 2
    args = arguments("state", "output")
    args[2] = args[0]  # Duplicate replacing a required option, not just appended.
    assert command.execute(args) == 2


SELECTIONS = [c for size in range(1, 4)
              for c in itertools.combinations(("characters", "words", "lines"), size)]


@pytest.mark.parametrize("metrics", SELECTIONS)
def test_mapping_and_option_order(metrics, tmp_path, monkeypatch, capsys):
    received = {}
    monkeypatch.setattr(command, "validate_roots", lambda *_: (tmp_path, tmp_path / "out"))
    monkeypatch.setattr(command, "create_stores", lambda path: path)
    class Session:
        def __init__(self, stores, **options):
            received.update(options)
        def create_objective(self, goal):
            assert goal == "plan configured trusted project"
            return SimpleNamespace(objective_id="test-id")
        def execute_intent(self, objective, intent):
            assert "Objective ID: test-id" in capsys.readouterr().out
            assert intent.metrics == metrics and intent.version == 2
            return SimpleNamespace(completed=True)
    monkeypatch.setattr(command, "OperationalSession", Session)
    args = arguments("state", "output", ",".join(reversed(metrics)))
    pairs = list(zip(args[::2], args[1::2]))
    assert command.execute([v for pair in reversed(pairs) for v in pair]) == 0
    assert received == {"python_project_workspace": tmp_path / "out",
                        "enabled_python_projects": ("text_stats_project_v2",)}


def test_every_option_order_and_abbreviations():
    args = arguments("state", "output")
    pairs = list(zip(args[::2], args[1::2]))
    for order in itertools.permutations(pairs):
        assert command.parse([v for pair in order for v in pair])[2].metrics == ("words", "lines")
    args[0] = "--work"
    assert command.execute(args) == 2
    args = arguments("state", "output")
    args[1] = "--unknown"
    assert command.execute(args) == 2


@pytest.mark.parametrize("mode", ["missing", "relative", "equal", "ancestor", "descendant", "case", "file"])
def test_root_refusal_before_stores(mode, tmp_path, monkeypatch):
    state, output = tmp_path / "state", tmp_path / "output"
    state.mkdir(); output.mkdir()
    if mode == "missing":
        state = tmp_path / "missing"
    elif mode == "relative":
        state = Path("relative")
    elif mode == "equal":
        output = state
    elif mode == "ancestor":
        state = tmp_path
    elif mode == "descendant":
        output = tmp_path
    elif mode == "case":
        if sys.platform != "win32":
            pytest.skip("Windows case equivalence")
        output = Path(str(state).upper())
    else:
        state = tmp_path / "file"
        state.write_text("sentinel")
    before = snapshot(tmp_path)
    monkeypatch.setattr(command, "create_stores", lambda *_: pytest.fail("store accessed"))
    assert command.execute(arguments(state, output)) == 1
    assert snapshot(tmp_path) == before and not (tmp_path / "missing").exists()


@pytest.mark.parametrize("which", [0, 1])
def test_reparse_refused_before_resolution(which, tmp_path, monkeypatch):
    roots = [tmp_path / "state", tmp_path / "output"]
    for root in roots:
        root.mkdir()
    original = Path.lstat
    def lstat(path, *args, **kwargs):
        info = original(path, *args, **kwargs)
        if path == roots[which]:
            return SimpleNamespace(st_mode=info.st_mode, st_file_attributes=0x400)
        return info
    monkeypatch.setattr(Path, "lstat", lstat)
    monkeypatch.setattr(command, "create_stores", lambda *_: pytest.fail("store accessed"))
    assert command.execute(arguments(*roots)) == 1


def test_runtime_error_redacted_and_incomplete_not_success(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(command, "validate_roots", lambda *_: (tmp_path, tmp_path))
    monkeypatch.setattr(command, "create_stores", lambda *_: None)
    class Session:
        def __init__(self, *args, **kwargs): pass
        def create_objective(self, goal): return SimpleNamespace(objective_id="kept-id")
        def execute_intent(self, *args): raise RuntimeError("SENSITIVE_SENTINEL")
    monkeypatch.setattr(command, "OperationalSession", Session)
    assert command.execute(arguments("state", "out")) == 1
    captured = capsys.readouterr()
    assert "kept-id" in captured.out and "RuntimeError" in captured.err
    assert "SENSITIVE_SENTINEL" not in captured.out + captured.err
    monkeypatch.setattr(Session, "execute_intent", lambda *_: SimpleNamespace(completed=False))
    assert command.execute(arguments("state", "out")) == 1
    assert "Published directory" not in capsys.readouterr().out


@pytest.mark.skipif(sys.platform != "win32", reason="local Windows NTFS contract")
def test_fresh_cli_build_use_discovery_collision(tmp_path):
    import hashlib
    state, output = tmp_path / "state", tmp_path / "output"
    state.mkdir(); output.mkdir()
    repo = Path(__file__).resolve().parents[1]
    active = snapshot(repo / "data")
    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo / "src")
    def run(args, code):
        result = subprocess.run([sys.executable, *args], cwd=tmp_path, env=env,
                                capture_output=True, text=True, timeout=110)
        assert result.returncode == code, result.stderr
        return result.stdout
    args = ["-m", "qaos.main", "build-project", *arguments(state, output)]
    text = run(args, 0)
    assert "Status: completed" in text and "Metrics: words,lines" in text
    def records(name): return json.loads((state / name).read_text())
    saved = {name: records(name) for name in ("objectives.json", "plans.json", "queue.json")}
    identity = saved["objectives.json"][0]["objective_id"]
    assert f"Objective ID: {identity}" in text
    project = output / "Example"
    evidence = next(r["result"] for r in saved["queue.json"] if r.get("task_id"))
    assert evidence["metrics"] == ["words", "lines"] and evidence["published"]
    assert evidence["member_sha256"] == {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in project.iterdir()}
    before = snapshot(tmp_path)
    assert json.loads(run(["-E", "-s", "-B", str(project / "app.py"), "--text", "one two\nthree"], 0)) == {"words": 3, "lines": 2}
    listing = run(["-m", "qaos.main", "objectives", "--workspace", str(state)], 0)
    assert identity in listing and snapshot(tmp_path) == before
    published = snapshot(output)
    failure = run(args, 1)
    assert "Objective ID:" in failure and "Status: failed" in failure
    for name, original in saved.items():
        assert [r for r in records(name) if r.get("objective_id") == identity] == original
    failed = next(r for r in records("objectives.json") if r["objective_id"] != identity)
    assert failed["status"] == "failed"
    plan = next(r for r in records("plans.json") if r["objective_id"] == failed["objective_id"])
    assert plan["tasks"][0]["status"] == "failed"
    item = next(r for r in records("queue.json") if r.get("task_id") and r["objective_id"] == failed["objective_id"])
    assert item["status"] == item["action"]["status"] == "failed"
    before = snapshot(tmp_path)
    run(["-m", "qaos.main", "recover", "--workspace", str(state), failed["objective_id"]], 1)
    assert snapshot(tmp_path) == before and snapshot(output) == published
    assert snapshot(repo / "data") == active
