import hashlib
import json
import subprocess
import sys

import pytest

from qaos.application import OperationalSession
from qaos.capabilities import text_stats_cli_template as template
from qaos.planner import PythonTemplateIntent, Task
from qaos.storage import create_stores


def snapshot(root):
    return {str(p.relative_to(root)): (p.read_bytes(), p.stat().st_mtime_ns)
            for p in root.rglob("*") if p.is_file()}


def setup(root, enabled=("text_stats_cli_v1",)):
    output = root / "out"
    output.mkdir(parents=True)
    stores = create_stores(root / "state")
    session = OperationalSession(stores, python_file_workspace=output,
                                 enabled_python_templates=enabled)
    return output, stores, session


def intent(path="app.py"):
    return PythonTemplateIntent(path, template_id="text_stats_cli_v1")


def test_public_build_and_standalone_process(tmp_path, capsys):
    output, stores, session = setup(tmp_path)
    obj = session.create_objective("plan CLI utility")
    assert session.execute_intent(obj, intent()).completed
    source = (output / "app.py").read_bytes()
    assert source == template.SOURCE.encode("utf-8")
    row = next(r for r in stores.queue_db.load() if r.get("task_id"))
    assert row["result"]["cli_cases_passed"] == 15
    assert row["result"]["source_sha256"] == hashlib.sha256(source).hexdigest()
    assert row["result"]["template_id"] == "text_stats_cli_v1"
    assert row["result"]["template_version"] == 1
    assert Task.from_dict(stores.plan_db.load()[0]["tasks"][0]).intent == intent()
    before = snapshot(output)
    # -I excludes repo/PYTHONPATH and user site: generated app is standalone.
    result = subprocess.run([sys.executable, "-I", str(output / "app.py"),
                             "--text", "one two\nthree"], cwd=output,
                            capture_output=True, text=True, timeout=5, shell=False)
    assert result.returncode == 0 and result.stderr == ""
    assert json.loads(result.stdout) == {"characters": 13, "words": 3, "lines": 2}
    capsys.readouterr()
    namespace = {"__name__": "imported_app"}
    exec(compile(source, "app.py", "exec"), namespace)
    assert capsys.readouterr().out == ""
    assert snapshot(output) == before


@pytest.mark.parametrize("enabled", [(), ("text_stats_v1",)])
def test_old_permissions_do_not_enable_cli(tmp_path, enabled):
    _, _, session = setup(tmp_path, enabled)
    obj = session.create_objective("plan disabled CLI")
    before = snapshot(tmp_path)
    with pytest.raises(ValueError, match="not enabled"):
        session.execute_intent(obj, intent())
    assert snapshot(tmp_path) == before


@pytest.mark.parametrize("path", ["../escape.py", "missing/app.py", "app.txt"])
def test_confined_output_failure(tmp_path, path):
    output, stores, session = setup(tmp_path)
    obj = session.create_objective("plan invalid output")
    with pytest.raises(ValueError):
        session.execute_intent(obj, intent(path))
    assert obj.status == "failed" and not list(output.iterdir())


def test_corrupt_cli_rejected_despite_valid_selftest_and_reload_denied(tmp_path, monkeypatch):
    # Simulate a trusted-source implementation bug, not just byte tampering:
    # no-argument self-test still passes; independent CLI cases must catch it.
    broken = template.SOURCE.replace("json.dumps(text_stats(text), sort_keys=True)",
                                     "json.dumps({}, sort_keys=True)")
    assert broken != template.SOURCE
    monkeypatch.setattr(template, "SOURCE", broken)
    output, stores, session = setup(tmp_path)
    obj = session.create_objective("plan corrupt CLI")
    with pytest.raises(RuntimeError, match="CLI acceptance failed"):
        session.execute_intent(obj, intent())
    item = next(r for r in stores.queue_db.load() if r.get("task_id"))
    assert item["result"]["stdout"] == template.SUCCESS_MARKER
    assert item["result"]["cli_cases_passed"] == 0
    assert item["status"] == item["action"]["status"] == "failed"
    assert stores.plan_db.load()[0]["tasks"][0]["status"] == obj.status == "failed"
    for options in ({}, {"python_file_workspace": output},
                    {"python_file_workspace": output, "enabled_python_templates": ("text_stats_v1",)}):
        before = snapshot(tmp_path)
        with pytest.raises(ValueError, match="not enabled"):
            OperationalSession(stores, **options).recover_objective(obj.objective_id)
        assert snapshot(tmp_path) == before
    before = snapshot(output)
    with pytest.raises(FileExistsError):
        session.recover_objective(obj.objective_id)
    assert snapshot(output) == before


def test_cli_and_old_template_isolation(tmp_path):
    output, stores, first = setup(tmp_path / "first")
    _, _, second = setup(tmp_path / "second", ("text_stats_v1",))
    before_second = snapshot(tmp_path / "second")
    first.execute_intent(first.create_objective("plan app"), intent())
    assert snapshot(tmp_path / "second") == before_second
    before = snapshot(output)
    with pytest.raises(FileExistsError):
        first.execute_intent(first.create_objective("plan collision"), intent())
    assert snapshot(output) == before
    assert second.execute_intent(second.create_objective("plan module"),
                                 PythonTemplateIntent("stats.py")).completed
