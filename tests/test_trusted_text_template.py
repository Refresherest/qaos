"""Public-session acceptance for the sole authorized trusted template."""

import hashlib

import pytest

from qaos.application import OperationalSession
from qaos.capabilities.python_template import PythonTemplateCapability
from qaos.capabilities.text_stats_template import SOURCE, SUCCESS_MARKER
from qaos.executive import create_executive
from qaos.planner import PythonFileIntent, PythonTemplateIntent, Task
from qaos.planner.intents import intent_from_dict
from qaos.storage import create_stores


def snapshot(root):
    return {str(p.relative_to(root)): (p.read_bytes(), p.stat().st_mtime_ns)
            for p in root.rglob("*") if p.is_file()}


def session_at(root, enabled=("text_stats_v1",)):
    output = root / "output"
    output.mkdir(parents=True, exist_ok=True)
    stores = create_stores(root / "state")
    session = OperationalSession(stores, python_file_workspace=output,
                                 enabled_python_templates=enabled)
    return output, stores, session


def test_public_template_build_evidence_and_import_contract(tmp_path, capsys):
    output, stores, session = session_at(tmp_path)
    objective = session.create_objective("plan text statistics module")
    result = session.execute_intent(objective, PythonTemplateIntent("stats.py"))
    assert result.completed and objective.status == "completed"
    assert len(result.plan.tasks) == 1
    content = (output / "stats.py").read_bytes()
    assert content == SOURCE.encode("utf-8")
    rows = [r for r in stores.queue_db.load() if r.get("task_id")]
    evidence = rows[0]["result"]
    assert evidence["template_id"] == "text_stats_v1"
    assert evidence["template_version"] == 1
    assert evidence["source_sha256"] == hashlib.sha256(content).hexdigest()
    assert evidence["stdout"] == SUCCESS_MARKER and evidence["exit_code"] == 0
    assert str(tmp_path) not in str(evidence)
    capsys.readouterr()
    namespace = {"__name__": "imported_statistics"}
    exec(compile(content, "stats.py", "exec"), namespace)
    assert capsys.readouterr().out == ""  # self-test is guarded on import
    assert namespace["text_stats"]("one two\nthree") == {"characters": 13, "words": 3, "lines": 2}
    for value in (None, 1, [], b"text"):
        with pytest.raises(TypeError):
            namespace["text_stats"](value)
    reloaded = Task.from_dict(stores.plan_db.load()[0]["tasks"][0])
    assert reloaded.intent == PythonTemplateIntent("stats.py")


@pytest.mark.parametrize("text,counts", [
    ("", (0, 0, 0)), ("hello world", (11, 2, 1)),
    (" a\t b  ", (7, 2, 1)), ("one\ntwo", (7, 2, 2)),
    ("a\r\nb\r\n", (6, 2, 2)), ("end\n", (4, 1, 1)),
    ("猫 café", (6, 2, 1)), ("e\u0301", (2, 1, 1)),
])
def test_independent_expected_counts(text, counts):
    namespace = {"__name__": "fixture_test"}
    exec(SOURCE, namespace)
    actual = namespace["text_stats"](text)
    assert actual == dict(zip(("characters", "words", "lines"), counts))


def test_self_test_rejects_corrupted_behavior_without_success_marker(capsys):
    corrupted = SOURCE.replace('"words": len(text.split())', '"words": 0')
    assert corrupted != SOURCE
    with pytest.raises(RuntimeError, match="acceptance failed"):
        exec(corrupted, {"__name__": "__main__"})
    assert SUCCESS_MARKER not in capsys.readouterr().out


def test_spoofed_marker_is_rejected_and_failure_recovery_is_coherent(tmp_path, monkeypatch):
    output, stores, session = session_at(tmp_path)
    original = PythonTemplateCapability._atomic_create
    def corrupt(target, content):
        original(target, b'print("QAOS text_stats_v1 PASS")\n')
    monkeypatch.setattr(PythonTemplateCapability, "_atomic_create", staticmethod(corrupt))
    objective = session.create_objective("plan corrupted template test")
    with pytest.raises(RuntimeError, match="reviewed source"):
        session.execute_intent(objective, PythonTemplateIntent("stats.py"))
    assert objective.status == "failed"
    before_output = snapshot(output)
    disabled = OperationalSession(stores, python_file_workspace=output)
    before = snapshot(tmp_path)
    with pytest.raises(ValueError, match="not enabled"):
        disabled.recover_objective(objective.objective_id)
    assert snapshot(tmp_path) == before
    with pytest.raises(ValueError, match="not enabled"):
        OperationalSession(stores).recover_objective(objective.objective_id)
    assert snapshot(tmp_path) == before
    reloaded = OperationalSession(stores, python_file_workspace=output,
                                  enabled_python_templates=("text_stats_v1",))
    with pytest.raises(FileExistsError):
        reloaded.recover_objective(objective.objective_id)
    assert snapshot(output) == before_output
    assert stores.objective_db.load()[0]["status"] == "failed"
    assert stores.plan_db.load()[0]["tasks"][0]["status"] == "failed"
    task = next(r for r in stores.queue_db.load() if r.get("task_id"))
    assert task["status"] == task["action"]["status"] == "failed"


def test_file_opt_in_alone_does_not_authorize_template(tmp_path):
    _, _, session = session_at(tmp_path, enabled=())
    objective = session.create_objective("plan disabled template")
    before = snapshot(tmp_path)
    with pytest.raises(ValueError, match="not enabled"):
        session.execute_intent(objective, PythonTemplateIntent("stats.py"))
    assert snapshot(tmp_path) == before and objective.status == "pending"


@pytest.mark.parametrize("enabled", [("unknown",), "text_stats_v1", None])
def test_bad_allowlists_rejected_before_writes(tmp_path, enabled):
    stores = create_stores(tmp_path / "state")
    before = snapshot(tmp_path)
    with pytest.raises((TypeError, ValueError)):
        create_executive(stores, enabled_python_templates=enabled)
    assert snapshot(tmp_path) == before


def test_explicit_output_required_and_allowlist_is_copied(tmp_path):
    stores = create_stores(tmp_path / "state")
    with pytest.raises(ValueError, match="workspace"):
        create_executive(stores, enabled_python_templates=("text_stats_v1",))
    enabled = ["text_stats_v1"]
    _, _, session = session_at(tmp_path / "enabled", enabled)
    enabled.clear()
    obj = session.create_objective("plan copied authorization")
    assert session.execute_intent(obj, PythonTemplateIntent("stats.py")).completed


@pytest.mark.parametrize("change", [{"template_id": "unknown"}, {"version": 2},
    {"version": True}, {"source": "print('x')"}, {"expected_stdout": "forged"}])
def test_unknown_or_caller_controlled_intent_fields_rejected(change):
    data = PythonTemplateIntent("stats.py").to_dict()
    data.update(change)
    with pytest.raises((TypeError, ValueError)):
        intent_from_dict(data)


def test_template_runs_are_isolated_and_print_contract_unchanged(tmp_path):
    _, _, first = session_at(tmp_path / "first")
    _, _, second = session_at(tmp_path / "second")
    before_second = snapshot(tmp_path / "second")
    first.execute_intent(first.create_objective("plan module"), PythonTemplateIntent("stats.py"))
    assert snapshot(tmp_path / "second") == before_second
    source = "print('compatible')\n"
    old_intent = PythonFileIntent("print.py", source, "compatible\n")
    assert intent_from_dict(old_intent.to_dict()) == old_intent
    assert second.execute_intent(second.create_objective("plan print"), old_intent).completed
    with pytest.raises(ValueError, match="print-only"):
        PythonFileIntent("bad.py", SOURCE, SUCCESS_MARKER)
