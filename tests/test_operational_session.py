"""Application-facing operational-session verification."""

import pytest

from qaos.application import OperationalSession
from qaos.config import create_configuration
from qaos.storage import create_stores


class RecordingLogger:
    def __init__(self):
        self.messages = []

    def info(self, message):
        self.messages.append(message)


def test_operational_session_executes_goal_in_one_workspace(tmp_path) -> None:
    stores = create_stores(tmp_path / "workspace")
    logger = RecordingLogger()
    session = OperationalSession(
        stores,
        configuration=create_configuration(tmp_path / "runtime"),
        logger=logger,
    )

    result = session.execute_goal("  operational application objective  ")

    assert result.completed is True
    assert result.objective.goal == "operational application objective"
    assert result.objective.status == "completed"
    assert result.classification == "analyze_objective"
    assert result.assignment.name == "chief_technology_officer"
    assert stores.objective_db.load()[0]["status"] == "completed"
    assert len(stores.plan_db.load()) == 1
    assert len(stores.queue_db.load()) == 6
    assert len(stores.reflection_db.load()) == 1
    assert len(stores.memory_db.load()) == 1
    assert len(stores.knowledge_db.load()) == 1
    assert logger.messages == [
        "Executive executing 'operational application objective'",
        "Executive execution complete.",
    ]


def test_operational_session_classifies_unmatched_goal_as_general(tmp_path) -> None:
    session = OperationalSession(create_stores(tmp_path / "general"))

    result = session.execute_goal("ship the next useful thing")

    assert result.completed is True
    assert result.classification == "general_objective"


@pytest.mark.parametrize("goal", ["", "   "])
def test_operational_session_rejects_empty_goal_without_persistence(
    tmp_path,
    goal,
) -> None:
    stores = create_stores(tmp_path / "invalid")
    session = OperationalSession(stores)

    with pytest.raises(ValueError, match="non-empty string"):
        session.execute_goal(goal)

    assert stores.objective_db.load() == []


@pytest.mark.parametrize("goal", [None, 42])
def test_operational_session_rejects_non_string_goal_without_persistence(
    tmp_path,
    goal,
) -> None:
    stores = create_stores(tmp_path / "invalid-type")
    session = OperationalSession(stores)

    with pytest.raises(TypeError, match="goal must be a string"):
        session.execute_goal(goal)

    assert stores.objective_db.load() == []


def test_operational_sessions_isolate_workspaces(tmp_path) -> None:
    first_stores = create_stores(tmp_path / "first")
    second_stores = create_stores(tmp_path / "second")
    first = OperationalSession(first_stores)
    second = OperationalSession(second_stores)

    first.execute_goal("first workspace objective")

    assert len(first_stores.objective_db.load()) == 1
    assert second_stores.objective_db.load() == []
    assert second_stores.queue_db.load() == []
    assert second_stores.memory_db.load() == []


def test_operational_session_requires_explicit_stores() -> None:
    with pytest.raises(TypeError, match="Stores instance"):
        OperationalSession(object())


def test_operational_session_rejects_invalid_configuration(tmp_path) -> None:
    with pytest.raises(TypeError, match="Configuration instance"):
        OperationalSession(
            create_stores(tmp_path),
            configuration=object(),
        )
