"""Operational composition-root verification."""

from qaos.config import create_configuration
from qaos.council.registry import council_registry
from qaos.executive import create_executive
from qaos.kernel.kernel import Kernel
from qaos.objectives.manager import ObjectiveManager
from qaos.storage import create_stores


class RecordingLogger:
    def __init__(self):
        self.messages = []

    def info(self, message):
        self.messages.append(message)


def test_create_executive_runs_isolated_operational_graph(tmp_path) -> None:
    global_council = council_registry.all()
    stores = create_stores(tmp_path / "workspace")
    objectives = ObjectiveManager(stores=stores)
    logger = RecordingLogger()
    executive = create_executive(
        stores,
        objectives=objectives,
        logger=logger,
    )
    kernel = Kernel(
        configuration=create_configuration(tmp_path / "runtime"),
        executive=executive,
    )
    objective = objectives.create("operational composition objective")

    result = kernel.execute_objective(objective)

    assert result.completed is True
    assert result.classification == "analyze_objective"
    assert result.assignment.name == "chief_technology_officer"
    assert result.execution_report.success is True
    assert objective.status == "completed"
    assert stores.objective_db.load()[0]["status"] == "completed"
    assert len(stores.plan_db.load()) == 1
    assert len(stores.queue_db.load()) == 6
    assert all(item["status"] == "completed" for item in stores.queue_db.load())
    assert len(stores.reflection_db.load()) == 1
    assert len(stores.memory_db.load()) == 1
    assert len(stores.knowledge_db.load()) == 1
    assert logger.messages == [
        "Executive executing 'operational composition objective'",
        "Executive execution complete.",
    ]
    assert council_registry.all() == global_council
