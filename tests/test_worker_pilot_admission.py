"""Local admission checks for the one-file Python worker pilot (WO-174)."""

import hashlib

import pytest

from qaos.artifacts import ArtifactManager
from qaos.objectives import Objective
from qaos.planner import Task
from qaos.queue import QueueItem
from qaos.storage import create_stores
from qaos.workers.pilot_admission import PILOT_FILE_LIMIT, prepare_python_pilot


CANDIDATE_SOURCE = 'def answer():\n    return "café"\n'
ACCEPTANCE_SOURCE = 'assert True, "independent acceptance"\n'


def make_context(
    tmp_path,
    *,
    candidate_content=CANDIDATE_SOURCE,
    acceptance_content=ACCEPTANCE_SOURCE,
    candidate_provenance=None,
    acceptance_provenance=None,
):
    objective = Objective("Produce one Python pilot", objective_id="objective-1")
    task = Task("Build the pilot", task_id="task-1")
    item = QueueItem(objective, "pilot-worker", action=task)
    stores = create_stores(tmp_path)
    ids = iter(("candidate-1", "acceptance-1"))
    artifacts = ArtifactManager(stores=stores, id_generator=lambda: next(ids))

    def provenance(role):
        return {
            "objective_id": objective.objective_id,
            "task_id": task.task_id,
            "pilot_role": role,
        }

    candidate = artifacts.create(
        "pilot candidate", "python_candidate", "candidate-author",
        objective.goal, candidate_content,
        provenance("candidate") if candidate_provenance is None else candidate_provenance,
    )
    acceptance = artifacts.create(
        "pilot acceptance", "python_acceptance", "acceptance-author",
        objective.goal, acceptance_content,
        provenance("acceptance") if acceptance_provenance is None else acceptance_provenance,
    )
    return objective, task, item, artifacts, candidate, acceptance, stores


def prepare(context, candidate_id="candidate-1", acceptance_id="acceptance-1"):
    objective, task, item, artifacts, *_ = context
    return prepare_python_pilot(
        objective, task, item, artifacts, candidate_id, acceptance_id
    )


def test_canonical_package_uses_artifact_bytes_and_fixed_manifest(tmp_path):
    context = make_context(tmp_path)
    objective, task, item, _, candidate, acceptance, stores = context
    stored_before = stores.artifact_db.load()

    package = prepare(context)

    assert package.objective_id == objective.objective_id
    assert package.task_id == task.task_id
    assert package.candidate_artifact.as_dict() == {
        "artifact_id": candidate.artifact_id,
        "content_sha256": candidate.content_sha256,
    }
    assert package.acceptance_artifact.as_dict() == {
        "artifact_id": acceptance.artifact_id,
        "content_sha256": acceptance.content_sha256,
    }
    assert package.manifest() == [
        {
            "role": "acceptance",
            "path": "acceptance/acceptance.py",
            "size": len(ACCEPTANCE_SOURCE.encode("utf-8")),
            "sha256": hashlib.sha256(ACCEPTANCE_SOURCE.encode("utf-8")).hexdigest(),
        },
        {
            "role": "candidate",
            "path": "candidate/candidate.py",
            "size": len(CANDIDATE_SOURCE.encode("utf-8")),
            "sha256": hashlib.sha256(CANDIDATE_SOURCE.encode("utf-8")).hexdigest(),
        },
    ]
    assert tuple(member.payload for member in package.members) == (
        ACCEPTANCE_SOURCE.encode("utf-8"), CANDIDATE_SOURCE.encode("utf-8")
    )
    assert stores.artifact_db.load() == stored_before
    assert item.status == "pending"
    assert item.result is None


@pytest.mark.parametrize(
    "candidate_id, acceptance_id",
    [
        ("", "acceptance-1"),
        ("candidate-1", ""),
        ("missing-candidate", "acceptance-1"),
        ("candidate-1", "missing-acceptance"),
        ("candidate-1", "candidate-1"),
    ],
)
def test_missing_or_duplicate_artifact_identity_is_rejected(
    tmp_path, candidate_id, acceptance_id
):
    context = make_context(tmp_path)
    with pytest.raises(ValueError):
        prepare(context, candidate_id, acceptance_id)


def test_missing_objective_or_task_identity_is_rejected(tmp_path):
    context = make_context(tmp_path)
    _, task, _, artifacts, *_ = context
    anonymous_objective = Objective("Produce one Python pilot")
    item = QueueItem(anonymous_objective, "pilot-worker", action=task)
    with pytest.raises(ValueError, match="objective_id"):
        prepare_python_pilot(
            anonymous_objective, task, item, artifacts,
            "candidate-1", "acceptance-1",
        )

    objective = context[0]
    anonymous_task = Task("Build the pilot")
    item = QueueItem(objective, "pilot-worker", action=anonymous_task)
    with pytest.raises(ValueError, match="task_id"):
        prepare_python_pilot(
            objective, anonymous_task, item, artifacts,
            "candidate-1", "acceptance-1",
        )


@pytest.mark.parametrize("role", ["candidate", "acceptance"])
def test_artifact_digest_tampering_is_rejected(tmp_path, role):
    context = make_context(tmp_path)
    artifact = context[4] if role == "candidate" else context[5]
    artifact._content = artifact.content + "# altered after canonical creation\n"
    with pytest.raises(ValueError, match="digest"):
        prepare(context)


@pytest.mark.parametrize("field", ["objective_id", "task_id", "pilot_role"])
def test_artifact_provenance_must_correlate(tmp_path, field):
    provenance = {
        "objective_id": "objective-1",
        "task_id": "task-1",
        "pilot_role": "acceptance",
    }
    provenance[field] = "other"
    context = make_context(tmp_path, acceptance_provenance=provenance)
    with pytest.raises(ValueError, match="provenance"):
        prepare(context)


@pytest.mark.parametrize(
    "role, attribute, value",
    [
        ("candidate", "artifact_type", "python_acceptance"),
        ("acceptance", "artifact_type", "python_candidate"),
        ("candidate", "objective", "Unrelated objective"),
        ("acceptance", "objective", "Unrelated objective"),
    ],
)
def test_wrong_artifact_role_type_or_objective_is_rejected(
    tmp_path, role, attribute, value
):
    context = make_context(tmp_path)
    artifact = context[4] if role == "candidate" else context[5]
    setattr(artifact, attribute, value)
    with pytest.raises(ValueError):
        prepare(context)


def test_acceptance_requires_distinct_creator(tmp_path):
    context = make_context(tmp_path)
    context[5].creator = context[4].creator
    with pytest.raises(ValueError, match="distinct creators"):
        prepare(context)


@pytest.mark.parametrize("role", ["candidate", "acceptance"])
def test_empty_artifact_content_is_rejected(tmp_path, role):
    option = f"{role}_content"
    context = make_context(tmp_path, **{option: ""})
    with pytest.raises(ValueError, match="bounds"):
        prepare(context)


def test_pilot_size_limit_counts_utf8_bytes_not_characters(tmp_path):
    exact = make_context(tmp_path / "exact", candidate_content="é" * (PILOT_FILE_LIMIT // 2))
    assert prepare(exact).manifest()[1]["size"] == PILOT_FILE_LIMIT

    excessive = make_context(
        tmp_path / "excessive", candidate_content="é" * (PILOT_FILE_LIMIT // 2 + 1)
    )
    with pytest.raises(ValueError, match="bounds"):
        prepare(excessive)


def test_invalid_unicode_after_artifact_creation_is_rejected(tmp_path):
    context = make_context(tmp_path)
    context[4]._content = "\ud800"
    with pytest.raises(ValueError, match="UTF-8"):
        prepare(context)


@pytest.mark.parametrize(
    "change",
    [
        lambda item, task: setattr(item, "objective_id", "wrong-objective"),
        lambda item, task: setattr(item, "objective", "Wrong goal"),
        lambda item, task: setattr(item, "task_id", "wrong-task"),
        lambda item, task: setattr(item, "action", Task("copy", task_id=task.task_id)),
        lambda item, task: setattr(item, "status", "running"),
        lambda item, task: setattr(item, "status", "completed"),
        lambda item, task: setattr(item, "result", {"previous": "attempt"}),
    ],
)
def test_queue_item_must_be_correlated_and_unattempted(tmp_path, change):
    context = make_context(tmp_path)
    task, item = context[1], context[2]
    change(item, task)
    with pytest.raises(ValueError):
        prepare(context)
