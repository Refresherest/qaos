"""Artifact identity, digest and provenance contract tests for WO-171."""

from types import MappingProxyType

import pytest

from qaos.artifacts import Artifact, ArtifactManager
from qaos.storage import create_stores


def deterministic_ids(*values):
    generated = iter(values)
    return lambda: next(generated)


def create(manager, title="artifact", content="café", provenance=None):
    return manager.create(title, "draft", "test", "objective", content, provenance)


def test_new_artifact_has_immutable_identity_utf8_digest_and_provenance(tmp_path):
    manager = ArtifactManager(
        stores=create_stores(tmp_path),
        id_generator=deterministic_ids("artifact-1"),
    )
    artifact = create(manager, provenance={"generator": "test", "run": "one"})

    assert artifact.artifact_id == "artifact-1"
    assert artifact.content_sha256 == (
        "850f7dc43910ff890f8879c0ed26fe697c93a067ad93a7d50f466a7028a9bf4e"
    )
    assert artifact.provenance == {"generator": "test", "run": "one"}
    assert isinstance(artifact.provenance, MappingProxyType)
    assert manager.get_by_id("artifact-1") is artifact

    with pytest.raises(ValueError, match="immutable"):
        artifact._assign_identity("artifact-2")
    with pytest.raises(AttributeError):
        artifact.content = "replacement"
    with pytest.raises(TypeError):
        artifact.provenance["run"] = "two"


def test_equal_titles_preserve_all_records_and_latest_title_lookup(tmp_path):
    stores = create_stores(tmp_path)
    manager = ArtifactManager(
        stores=stores,
        id_generator=deterministic_ids("artifact-1", "artifact-2"),
    )
    first = create(manager, title="repeat", content="first")
    second = create(manager, title="repeat", content="second")

    assert manager.get("repeat") is second
    assert manager.get(first) is first
    assert manager.get_by_id("artifact-1") is first
    assert manager.get_by_id("artifact-2") is second
    assert manager.artifact_records() == (first, second)
    assert [row["artifact_id"] for row in stores.artifact_db.load()] == [
        "artifact-1",
        "artifact-2",
    ]

    reloaded = ArtifactManager(
        stores=stores,
        id_generator=lambda: pytest.fail("reload must not generate identity"),
    )
    assert reloaded.get("repeat").artifact_id == "artifact-2"
    assert reloaded.get_by_id("artifact-1").content == "first"
    assert len(reloaded.artifact_records()) == 2


def test_duplicate_identity_fails_closed_before_persistence(tmp_path):
    stores = create_stores(tmp_path)
    manager = ArtifactManager(
        stores=stores,
        id_generator=deterministic_ids("duplicate", "duplicate"),
    )
    create(manager, title="first")
    original = stores.artifact_db.load()

    with pytest.raises(ValueError, match="duplicate artifact_id"):
        create(manager, title="second")

    assert stores.artifact_db.load() == original
    assert manager.get("second") is None


def test_duplicate_persisted_identity_fails_closed_on_load(tmp_path):
    stores = create_stores(tmp_path)
    rows = []
    for title in ("first", "second"):
        rows.append({
            "title": title,
            "artifact_type": "draft",
            "creator": "test",
            "objective": "objective",
            "content": title,
            "artifact_id": "duplicate",
        })
    stores.artifact_db.save(rows)

    with pytest.raises(ValueError, match="duplicate artifact_id"):
        ArtifactManager(stores=stores)


def test_legacy_load_and_save_does_not_write_forward(tmp_path):
    stores = create_stores(tmp_path)
    legacy = {
        "title": "legacy",
        "artifact_type": "draft",
        "creator": "test",
        "objective": "objective",
        "content": "legacy content",
    }
    stores.artifact_db.save([legacy])
    manager = ArtifactManager(
        stores=stores,
        id_generator=lambda: pytest.fail("legacy load must not generate identity"),
    )

    artifact = manager.get("legacy")
    manager._save()

    assert artifact.artifact_id is None
    assert manager.get_by_id("legacy") is None
    assert stores.artifact_db.load() == [legacy]


@pytest.mark.parametrize(
    "provenance, error",
    [
        ({str(index): "value" for index in range(17)}, "too many entries"),
        ({"k" * 65: "value"}, "key is too long"),
        ({"key": "v" * 1025}, "value is too long"),
        ({"key": ""}, "values must be non-empty strings"),
        ({"key": 1}, "values must be non-empty strings"),
        (
            {str(index): "é" * 512 for index in range(8)},
            "provenance is too large",
        ),
    ],
)
def test_provenance_bounds_fail_closed(tmp_path, provenance, error):
    manager = ArtifactManager(stores=create_stores(tmp_path))

    with pytest.raises(ValueError, match=error):
        create(manager, provenance=provenance)


def test_content_and_persisted_digest_must_match(tmp_path):
    with pytest.raises(TypeError, match="content must be a string"):
        Artifact("bad", "draft", "test", "objective", b"bytes")

    stores = create_stores(tmp_path)
    stores.artifact_db.save([{
        "title": "tampered",
        "artifact_type": "draft",
        "creator": "test",
        "objective": "objective",
        "content": "content",
        "artifact_id": "artifact-1",
        "content_sha256": "0" * 64,
        "provenance": {},
    }])

    with pytest.raises(ValueError, match="does not match"):
        ArtifactManager(stores=stores)
