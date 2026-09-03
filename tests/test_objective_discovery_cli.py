"""OWNER-DECISION-019 read-only Objective discovery tests."""

import json
from pathlib import Path

import pytest

from qaos.main import main
from qaos.storage import create_stores


def fingerprint(path):
    return {p.name: (p.read_bytes(), p.stat().st_mtime_ns)
            for p in path.iterdir() if p.is_file()}


@pytest.mark.parametrize("args", [[], ["--workspace"],
    ["--workspace", "x", "extra"], ["--other", "x"],
    ["--workspace", " "]])
def test_invalid_usage_never_delegates(args, monkeypatch, capsys):
    monkeypatch.setattr("qaos.commands.objectives.execute",
                        lambda value: pytest.fail("must not delegate"))
    assert main(["objectives", *args]) == 2
    assert "Usage:" in capsys.readouterr().err


def test_missing_workspace_not_created(tmp_path, capsys):
    missing = tmp_path / "missing"
    assert main(["objectives", "--workspace", str(missing)]) == 1
    assert not missing.exists()
    assert "Traceback" not in capsys.readouterr().err


def test_empty_existing_workspace_stays_empty(tmp_path, capsys):
    before = fingerprint(tmp_path)
    assert main(["objectives", "--workspace", str(tmp_path)]) == 0
    assert capsys.readouterr().out == "Objectives: []\n"
    assert fingerprint(tmp_path) == before


def test_complete_order_legacy_repeats_and_escaping_are_read_only(tmp_path, capsys):
    stores = create_stores(tmp_path)
    stores.objective_db.save([
        {"goal": "repeat\n\x1b[31m", "objective_id": "id-1", "status": "failed"},
        {"goal": "repeat\n\x1b[31m", "status": "pending"},
        {"goal": "third", "objective_id": "id-3", "status": "completed"},
    ])
    before = fingerprint(tmp_path)
    assert main(["objectives", "--workspace", str(tmp_path)]) == 0
    output = capsys.readouterr().out
    rows = [json.loads(line) for line in output.splitlines()[1:]]
    assert [row["objective_id"] for row in rows] == ["id-1", None, "id-3"]
    assert [row["goal"] for row in rows] == ["repeat\n\x1b[31m",
                                              "repeat\n\x1b[31m", "third"]
    assert "\x1b" not in output and "\\u001b" in output
    assert fingerprint(tmp_path) == before


@pytest.mark.parametrize("content", ["not-json", '[{"goal":"a","objective_id":"x"},'
    '{"goal":"b","objective_id":"x"}]'])
def test_invalid_or_duplicate_data_has_no_partial_output(tmp_path, capsys, content):
    (tmp_path / "objectives.json").write_text(content, encoding="utf-8")
    before = fingerprint(tmp_path)
    assert main(["objectives", "--workspace", str(tmp_path)]) == 1
    captured = capsys.readouterr()
    assert captured.out == "" and "Traceback" not in captured.err
    assert fingerprint(tmp_path) == before


def test_only_objective_store_is_read(monkeypatch, tmp_path):
    from qaos.storage.json_store import JSONStore
    original = JSONStore.load
    paths = []
    def record(store):
        paths.append(Path(store.path).name)
        return original(store)
    monkeypatch.setattr(JSONStore, "load", record)
    assert main(["objectives", "--workspace", str(tmp_path)]) == 0
    assert paths == ["objectives.json"]
