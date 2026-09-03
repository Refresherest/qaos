"""One-shot CLI adapter for an operational QAOS objective."""

from qaos.application import OperationalSession
from qaos.storage import create_stores


def execute(workspace, goal):
    """Execute goal in the explicitly selected workspace and print a summary."""
    session = OperationalSession(create_stores(workspace))
    objective = session.create_objective(goal)
    print(f"Objective ID: {objective.objective_id}", flush=True)
    result = session.execute_objective(objective)
    assignment = getattr(result, "assignment", None)

    print(f"Objective: {result.objective.goal}")
    print(f"Status: {'completed' if result.completed else 'failed'}")
    print(f"Classification: {result.classification}")
    print(f"Assignee: {getattr(assignment, 'name', None)}")

    return result
