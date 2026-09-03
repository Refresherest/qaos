"""Public-session acceptance checks for OWNER-DECISION-024."""

import subprocess

import pytest

from qaos.application import OperationalSession
from qaos.planner import PythonFileIntent
from qaos.storage import create_stores


def intent():
    return PythonFileIntent("built.py", "print('QAOS built this')\n", "QAOS built this\n")


def setup_session(tmp_path, enabled=True):
    output = tmp_path / "output"
    output.mkdir(parents=True)
    stores = create_stores(tmp_path / "state")
    session = OperationalSession(stores, **({"python_file_workspace": output} if enabled else {}))
    objective = session.create_objective("plan a deterministic program")
    return output, stores, session, objective


def snapshot(root):
    return {str(p.relative_to(root)): (p.read_bytes(), p.stat().st_mtime_ns)
            for p in root.rglob("*") if p.is_file()}


def test_public_session_builds_and_runs_all_pipeline_stages(tmp_path):
    output, stores, session, objective = setup_session(tmp_path)
    result = session.execute_intent(objective, intent())
    assert result.objective is objective
    assert result.completed and objective.status == "completed"
    assert result.classification is not None and result.assignment is not None
    assert len(result.plan.tasks) == 1
    assert result.plan.tasks[0].task_id
    assert result.plan.tasks[0].intent == intent()
    assert result.execution_report.success
    assert result.reflection is not None
    assert stores.memory_db.load() and stores.knowledge_db.load()
    assert (output / "built.py").read_text(encoding="utf-8") == intent().source
    tasks = [row for row in stores.queue_db.load() if row.get("task_id")]
    assert len(tasks) == 1 and tasks[0]["result"]["stdout"] == intent().expected_stdout
    assert tasks[0]["status"] == "completed"
    before = snapshot(tmp_path)
    with pytest.raises(ValueError, match="pending"):
        session.execute_intent(objective, intent())
    assert snapshot(tmp_path) == before


@pytest.mark.parametrize("case", ["disabled", "foreign", "bad_intent", "status", "existing_plan"])
def test_invalid_submission_does_not_write_execution_state(tmp_path, case):
    _output, stores, session, objective = setup_session(tmp_path, enabled=case != "disabled")
    supplied_intent = intent()
    if case == "foreign":
        _, _, other, objective = setup_session(tmp_path / "other")
    elif case == "bad_intent":
        supplied_intent = object()
    elif case == "status":
        objective.status = "failed"
    elif case == "existing_plan":
        session._executive._intent_planner.create(objective)
    before = snapshot(tmp_path)
    with pytest.raises((RuntimeError, ValueError, TypeError)):
        session.execute_intent(objective, supplied_intent)
    assert snapshot(tmp_path) == before


def test_verifier_failure_persists_failed_lifecycle_and_refuses_replacement(tmp_path, monkeypatch):
    output, stores, session, objective = setup_session(tmp_path)
    monkeypatch.setattr(subprocess, "run", lambda *args, **kw: subprocess.CompletedProcess(args[0], 1))
    with pytest.raises(RuntimeError, match="verification failed"):
        session.execute_intent(objective, intent())
    assert objective.status == "failed"
    assert stores.plan_db.load()[0]["tasks"][0]["status"] == "failed"
    assert (output / "built.py").exists()
    reloaded = OperationalSession(stores, python_file_workspace=output)
    with pytest.raises(FileExistsError):
        reloaded.recover_objective(objective.objective_id)
    assert stores.objective_db.load()[0]["status"] == "failed"
    assert stores.plan_db.load()[0]["tasks"][0]["status"] == "failed"
    task_items = [row for row in stores.queue_db.load() if row.get("task_id")]
    assert task_items[0]["status"] == task_items[0]["action"]["status"] == "failed"


def test_existing_output_failure_preserves_truthful_task_state(tmp_path):
    output, stores, session, objective = setup_session(tmp_path)
    (output / "built.py").write_text("existing", encoding="utf-8")
    with pytest.raises(FileExistsError):
        session.execute_intent(objective, intent())
    assert objective.status == "failed"
    assert stores.plan_db.load()[0]["tasks"][0]["status"] == "failed"
    assert (output / "built.py").read_text(encoding="utf-8") == "existing"
    task_items = [row for row in stores.queue_db.load() if row.get("task_id")]
    assert task_items[0]["status"] == task_items[0]["action"]["status"] == "failed"


def test_sessions_and_ordinary_execution_remain_isolated(tmp_path):
    first_output, _, first, objective = setup_session(tmp_path / "first")
    _, _, second, other = setup_session(tmp_path / "second")
    before = snapshot(tmp_path / "second")
    first.execute_intent(objective, intent())
    assert snapshot(tmp_path / "second") == before
    first_files = snapshot(first_output)
    result = second.execute_objective(other)
    assert result.completed
    assert all(task.intent is None for task in result.plan.tasks)
    assert snapshot(first_output) == first_files


def test_pre_execution_failure_keeps_original_exception_and_fails_objective(tmp_path, monkeypatch):
    _, stores, session, objective = setup_session(tmp_path)
    failure = RuntimeError("controlled planning failure")
    def fail_plan(*args):
        raise failure
    monkeypatch.setattr(session._executive._intent_planner, "plan_intent", fail_plan)
    with pytest.raises(RuntimeError) as caught:
        session.execute_intent(objective, intent())
    assert caught.value is failure
    assert objective.status == stores.objective_db.load()[0]["status"] == "failed"
