"""Data-integrity tests for the active JSON storage primitive."""

import pytest

from qaos.storage.json_store import JSONStore, StorageDataError


def test_json_store_round_trip_uses_atomic_target(tmp_path) -> None:
    path = tmp_path / "nested" / "records.json"
    store = JSONStore(path)

    store.save([{"id": "one"}])

    assert store.load() == [{"id": "one"}]
    assert not path.with_suffix(".json.tmp").exists()


def test_json_store_rejects_nonempty_corrupt_json(tmp_path) -> None:
    path = tmp_path / "records.json"
    path.write_text("{not-json}", encoding="utf-8")

    with pytest.raises(StorageDataError):
        JSONStore(path).load()


def test_json_store_treats_blank_file_as_empty_initial_state(tmp_path) -> None:
    path = tmp_path / "records.json"
    path.write_text("", encoding="utf-8")

    assert JSONStore(path).load() == []
