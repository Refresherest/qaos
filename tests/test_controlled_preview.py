import itertools
import json
import os
from pathlib import Path
import socket
import subprocess
import sys

import pytest
from qaos.commands import preview_project
from qaos.main import main
from qaos.planner.controlled_brief import interpret
from qaos.planner.intents import intent_from_dict


ORDER = ("characters", "words", "lines")
SEQUENCES = [p for size in range(1, 4) for p in itertools.permutations(ORDER, size)]


@pytest.mark.parametrize("metrics", SEQUENCES)
@pytest.mark.parametrize("variant", ["normal", "upper", "spaces"])
def test_all_sequences(metrics, variant, capsys):
    brief = "count " + " and ".join(metrics)
    if variant == "upper": brief = brief.upper()
    if variant == "spaces": brief = "  " + brief.replace(" ", "   ") + " "
    expected = {"type": "python_project", "version": 2,
                "template_id": "text_stats_project_v2", "relative_directory": "Example",
                "metrics": [m for m in ORDER if m in metrics]}
    intent = interpret("Example", brief)
    assert intent.to_dict() == expected and intent_from_dict(expected) == intent
    assert main(["preview-project", "--brief", brief, "--directory", "Example"]) == 0
    captured = capsys.readouterr()
    assert not captured.err and captured.out.endswith("\n")
    assert len(captured.out.splitlines()) == 1
    assert json.loads(captured.out) == {"status": "preview", "grammar_version": 1, "intent": expected}


@pytest.mark.parametrize("brief", [None, 12, [], {}, "", " ", "x" * 257,
    "count words and words", "count word", "count", "words", "count and words",
    "count words and", "count words lines", "count words but not lines",
    "count words and publish it", "please count words", "count words.",
    "count words\n", "count\twords", "count words\r", "count\x00words",
    "count wоrds", "count words\u00a0", "count words; echo secret", "count words and lines and characters and words"])
def test_refused_grammar(brief):
    with pytest.raises((TypeError, ValueError)):
        interpret("Example", brief)


def test_exact_length_boundary():
    assert interpret("Example", "count words" + " " * 245).metrics == ("words",)
    with pytest.raises(ValueError): interpret("Example", "count words" + " " * 246)


@pytest.mark.parametrize("directory", ["", "../Example", "CON", "two names", "/abs", "a" * 65, None])
def test_directory_contract(directory):
    with pytest.raises(ValueError): interpret(directory, "count words")


@pytest.mark.parametrize("args", [[], ["--directory"], ["--directory", "Example"],
    ["--directory", "Example", "--directory", "Other"],
    ["--brief", "count words", "--brief", "count lines"],
    ["--dir", "Example", "--brief", "count words"],
    ["--directory", "Example", "--unknown", "value"],
    ["--directory", "Example", "--brief", ""],
    ["--directory", " ", "--brief", "count words"],
    ["--directory", "Example", "--brief", "count words", "extra"],
    ["--directory", "--brief", "--brief", "count words"],
    ["--workspace", "somewhere", "--brief", "count words"],
    ["--directory", "Example", "--brief", "SENSITIVE_SENTINEL"],
    ["--directory", "../bad", "--brief", "count words"]])
def test_cli_refusal(args, capsys):
    assert main(["preview-project", *args]) == 2
    captured = capsys.readouterr()
    assert captured.out == "" and captured.err == preview_project.DIAGNOSTIC + "\n"
    assert "SENSITIVE_SENTINEL" not in captured.err


def test_unexpected_error_is_redacted(monkeypatch, capsys):
    def fail(*_): raise RuntimeError("SENSITIVE_SENTINEL")
    monkeypatch.setattr(preview_project, "interpret", fail)
    assert main(["preview-project", "--directory", "Example", "--brief", "count words"]) == 1
    captured = capsys.readouterr()
    assert captured.out == "" and captured.err == "Project preview failed (RuntimeError).\n"


def test_no_execution_or_stores(monkeypatch, capsys):
    import qaos.storage
    from qaos.application import OperationalSession
    from qaos.commands import build_project
    def forbidden(*args, **kwargs): pytest.fail("preview attempted side effect")
    monkeypatch.setattr(qaos.storage, "create_stores", forbidden)
    monkeypatch.setattr(OperationalSession, "__init__", forbidden)
    monkeypatch.setattr(build_project, "execute", forbidden)
    monkeypatch.setattr(build_project, "validate_roots", forbidden)
    monkeypatch.setattr(subprocess, "Popen", forbidden)
    monkeypatch.setattr(socket, "socket", forbidden)
    monkeypatch.setattr(os, "system", forbidden)
    assert main(["preview-project", "--directory", "Example", "--brief", "count words"]) == 0
    assert json.loads(capsys.readouterr().out)["status"] == "preview"


def snapshot(root):
    return {str(p.relative_to(root)): (p.read_bytes(), p.stat().st_mtime_ns)
            for p in root.rglob("*") if p.is_file()}


def test_fresh_preview_no_writes_and_separate_build(tmp_path):
    repo = Path(__file__).resolve().parents[1]
    state, output = tmp_path / "state", tmp_path / "output"
    state.mkdir(); output.mkdir()
    active = snapshot(repo / "data")
    before = snapshot(tmp_path)
    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo / "src")
    def run(args, expected):
        result = subprocess.run([sys.executable, "-B", "-m", "qaos.main", *args],
                                cwd=tmp_path, env=env, capture_output=True, text=True, timeout=110)
        assert result.returncode == expected, result.stderr
        return result
    args = ["preview-project", "--directory", "Example", "--brief", "count lines and words"]
    result = run(args, 0)
    preview = json.loads(result.stdout)
    assert not result.stderr and preview["intent"]["metrics"] == ["words", "lines"]
    args[-1] = "count words and publish it"
    refusal = run(args, 2)
    assert not refusal.stdout and refusal.stderr == preview_project.DIAGNOSTIC + "\n"
    assert snapshot(tmp_path) == before and list(state.iterdir()) == list(output.iterdir()) == []
    assert {p.name for p in tmp_path.iterdir()} == {"state", "output"}
    assert snapshot(repo / "data") == active
    if sys.platform != "win32": return  # Preview is pure; existing builder is Windows-only.
    build = ["build-project", "--workspace", str(state), "--output-root", str(output),
             "--directory", "Example", "--metrics", "words,lines"]
    run(build, 2)  # A successful preview has not granted permission.
    assert snapshot(tmp_path) == before
    build += ["--enable-project", "text_stats_project_v2"]
    run(build, 0)  # Deliberately separate operator request; not preview loading.
    plans = json.loads((state / "plans.json").read_text())
    assert plans[0]["tasks"][0]["intent"] == preview["intent"]
    published = snapshot(output)
    collision = run(build, 1)
    assert "FileExistsError" in collision.stderr and snapshot(output) == published
    assert snapshot(repo / "data") == active
