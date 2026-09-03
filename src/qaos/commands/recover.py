"""One-shot adapter for explicitly selected workspace recovery."""

from pathlib import Path

from qaos.application import OperationalSession
from qaos.storage import create_stores


def execute(workspace, objective_id):
    """Recover exactly one existing Objective; never create a missing workspace."""
    if not Path(workspace).is_dir():
        raise ValueError("Recovery requires an existing workspace directory")

    objective = OperationalSession(create_stores(workspace)).recover_objective(
        objective_id
    )
    if objective.status != "completed":
        raise RuntimeError("Recovery did not complete the Objective")

    print(f"Objective ID: {objective.objective_id}")
    print(f"Objective: {objective.goal}")
    print(f"Status: {objective.status}")
    return objective
