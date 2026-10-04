"""Local admission package for one independently tested Python pilot.

This module derives immutable byte manifests from canonical QAOS Artifacts. It
does not contact a worker, execute code, mutate a QueueItem, or persist state.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field


PILOT_FILE_LIMIT = 64 * 1024
PILOT_PATHS = {
    "acceptance": "acceptance/acceptance.py",
    "candidate": "candidate/candidate.py",
}
_DIGEST = re.compile(r"[0-9a-f]{64}\Z")


@dataclass(frozen=True)
class PilotArtifactRef:
    artifact_id: str
    content_sha256: str

    def as_dict(self) -> dict[str, str]:
        return {
            "artifact_id": self.artifact_id,
            "content_sha256": self.content_sha256,
        }


@dataclass(frozen=True)
class PilotMember:
    role: str
    path: str
    sha256: str
    payload: bytes = field(repr=False)

    def manifest(self) -> dict[str, str | int]:
        return {
            "role": self.role,
            "path": self.path,
            "size": len(self.payload),
            "sha256": self.sha256,
        }


@dataclass(frozen=True)
class PilotPackage:
    objective_id: str
    task_id: str
    candidate_artifact: PilotArtifactRef
    acceptance_artifact: PilotArtifactRef
    members: tuple[PilotMember, PilotMember] = field(repr=False)
    origin_item: object = field(repr=False, compare=False)

    def manifest(self) -> list[dict[str, str | int]]:
        return [member.manifest() for member in self.members]


def _identified(value, label: str) -> str:
    if not isinstance(value, str) or not value or len(value.encode("utf-8")) > 256:
        raise ValueError(f"{label} must be a bounded non-empty identity")
    return value


def _member(artifact, role: str, objective_id: str, task_id: str,
            objective_goal: str) -> tuple[PilotArtifactRef, PilotMember]:
    artifact_id = _identified(getattr(artifact, "artifact_id", None), f"{role} artifact_id")
    creator = _identified(getattr(artifact, "creator", None), f"{role} creator")
    if artifact.objective != objective_goal:
        raise ValueError(f"{role} artifact objective does not match")
    if artifact.artifact_type != f"python_{role}":
        raise ValueError(f"{role} artifact type does not match pilot role")
    provenance = artifact.provenance
    if (provenance.get("objective_id") != objective_id
            or provenance.get("task_id") != task_id
            or provenance.get("pilot_role") != role):
        raise ValueError(f"{role} artifact provenance does not correlate")
    if not isinstance(artifact.content, str):
        raise ValueError(f"{role} artifact content must be UTF-8 text")
    try:
        payload = artifact.content.encode("utf-8", "strict")
    except UnicodeEncodeError as error:
        raise ValueError(f"{role} artifact content must be UTF-8 text") from error
    if not 0 < len(payload) <= PILOT_FILE_LIMIT:
        raise ValueError(f"{role} artifact exceeds pilot file bounds")
    digest = hashlib.sha256(payload).hexdigest()
    if not isinstance(artifact.content_sha256, str) or not _DIGEST.fullmatch(artifact.content_sha256) or digest != artifact.content_sha256:
        raise ValueError(f"{role} artifact digest does not match bytes")
    return (
        PilotArtifactRef(artifact_id, digest),
        PilotMember(role, PILOT_PATHS[role], digest, payload),
    )


def prepare_python_pilot(objective, task, queue_item, artifacts,
                         candidate_artifact_id: str,
                         acceptance_artifact_id: str) -> PilotPackage:
    """Resolve canonical Artifacts and build a fixed two-member pilot package."""
    objective_id = _identified(getattr(objective, "objective_id", None), "objective_id")
    task_id = _identified(getattr(task, "task_id", None), "task_id")
    if (queue_item.objective_id != objective_id
            or queue_item.objective != objective.goal
            or queue_item.task_id != task_id
            or queue_item.action is not task
            or queue_item.action.task_id != task_id):
        raise ValueError("QueueItem does not correlate to canonical Objective/Task")
    if queue_item.status != "pending" or queue_item.result is not None:
        raise ValueError("pilot requires an unattempted pending QueueItem")
    candidate_artifact_id = _identified(candidate_artifact_id, "candidate artifact_id")
    acceptance_artifact_id = _identified(acceptance_artifact_id, "acceptance artifact_id")
    if candidate_artifact_id == acceptance_artifact_id:
        raise ValueError("candidate cannot author its own acceptance")
    candidate = artifacts.get_by_id(candidate_artifact_id)
    acceptance = artifacts.get_by_id(acceptance_artifact_id)
    if candidate is None or acceptance is None:
        raise ValueError("pilot Artifact identity is not present in canonical registry")
    if candidate.creator == acceptance.creator:
        raise ValueError("candidate and acceptance require distinct creators")
    candidate_ref, candidate_member = _member(candidate, "candidate", objective_id, task_id, objective.goal)
    acceptance_ref, acceptance_member = _member(acceptance, "acceptance", objective_id, task_id, objective.goal)
    return PilotPackage(
        objective_id, task_id, candidate_ref, acceptance_ref,
        (acceptance_member, candidate_member), queue_item,
    )
