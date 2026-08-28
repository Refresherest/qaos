"""One-shot CLI adapter for an operational QAOS objective."""

from qaos.application import OperationalSession
from qaos.storage import create_stores


def execute(workspace, goal):
    """Execute goal in the explicitly selected workspace and print a summary."""
    result = OperationalSession(create_stores(workspace)).execute_goal(goal)
    assignment = getattr(result, "assignment", None)

    print(f"Objective: {result.objective.goal}")
    print(f"Status: {'completed' if result.completed else 'failed'}")
    print(f"Classification: {result.classification}")
    print(f"Assignee: {getattr(assignment, 'name', None)}")

    return result
