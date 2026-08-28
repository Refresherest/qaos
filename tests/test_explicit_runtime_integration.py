"""End-to-end proof for an explicitly composed isolated QAOS runtime."""

from __future__ import annotations

from types import SimpleNamespace

from qaos.agents import Agent
from qaos.agents.manager import AgentManager
from qaos.agents.registry import AgentRegistry
from qaos.artifacts.manager import ArtifactManager
from qaos.capabilities.manager import CapabilityManager
from qaos.capabilities.registry import CapabilityRegistry
from qaos.capabilities.system import SystemCapability
from qaos.classifier import ClassifierManager, IntentClassifier
from qaos.config import create_configuration
from qaos.context.manager import ContextManager
from qaos.council.delegator import Delegator
from qaos.council.manager import CouncilManager
from qaos.council.registry import CouncilRegistry
from qaos.execution.engine import ExecutionEngine
from qaos.execution.manager import ExecutionManager
from qaos.execution.registry import ExecutionRegistry
from qaos.executive.manager import ExecutiveManager
from qaos.executive.orchestrator import ExecutiveOrchestrator
from qaos.executive.pipeline import ExecutivePipeline
from qaos.kernel.kernel import Kernel
from qaos.knowledge.manager import KnowledgeManager
from qaos.learning.engine import LearningEngine
from qaos.learning.learner import Learner
from qaos.learning.manager import LearningManager
from qaos.memory.manager import MemoryManager
from qaos.objectives.manager import ObjectiveManager
from qaos.planner.generator import PlanGenerator
from qaos.planner.manager import PlannerManager
from qaos.queue.manager import QueueManager
from qaos.reflection.manager import ReflectionManager
from qaos.retrieval.engine import RetrievalEngine
from qaos.retrieval.manager import RetrievalManager
from qaos.skills import Skill
from qaos.skills.manager import SkillManager
from qaos.skills.registry import SkillRegistry
from qaos.skills.resolver import SkillResolver
from qaos.storage import create_stores
from qaos.workers.default import DefaultWorker
from qaos.workers.manager import WorkerManager
from qaos.workers.registry import WorkerRegistry


class RecordingLogger:
    def __init__(self):
        self.messages = []

    def info(self, message):
        self.messages.append(message)


def test_kernel_runs_fully_explicit_isolated_runtime(tmp_path) -> None:
    stores = create_stores(tmp_path / "workspace")
    memory = MemoryManager(stores=stores)
    knowledge = KnowledgeManager(stores=stores)
    artifacts = ArtifactManager(stores=stores)
    objectives = ObjectiveManager(stores=stores)

    capabilities = CapabilityManager(registry=CapabilityRegistry())
    capabilities.register(SystemCapability())
    skills = SkillRegistry()
    SkillManager(registry=skills).register(
        Skill("planning", "system", capabilities=capabilities)
    )
    agents = AgentManager(registry=AgentRegistry())
    agents.register(Agent("default", resolver=SkillResolver(registry=skills)))
    workers = WorkerManager(
        registry=WorkerRegistry(),
        default=DefaultWorker(agents=agents),
    )
    queue = QueueManager(stores=stores, workers=workers)

    council_registry = CouncilRegistry()
    member = SimpleNamespace(
        name="chief_technology_officer",
        title="Isolated CTO",
    )
    council_registry.register(member)
    council = CouncilManager(
        registry=council_registry,
        delegator_service=Delegator(
            registry=council_registry,
            objectives=objectives,
        ),
        queue=queue,
    )

    context = ContextManager(
        retrieval=RetrievalManager(
            engine=RetrievalEngine(
                memory=memory,
                knowledge=knowledge,
                artifacts=artifacts,
            )
        )
    )
    planner = PlannerManager(
        stores=stores,
        generator=PlanGenerator(context=context),
    )
    execution_registry = ExecutionRegistry()
    execution_registry.register(
        "default",
        ExecutionEngine(planner=planner, queue=queue),
    )
    execution = ExecutionManager(
        registry=execution_registry,
        objectives=objectives,
    )

    classifier_service = IntentClassifier()
    classifier_service.register("objective", "analyze_objective")
    pipeline = ExecutivePipeline(
        classifier=ClassifierManager(classifier_service=classifier_service),
        council=council,
        planner=planner,
        execution=execution,
        reflection=ReflectionManager(stores=stores),
        learning=LearningManager(
            learner_service=Learner(
                engine=LearningEngine(memory=memory, knowledge=knowledge)
            )
        ),
    )
    logger = RecordingLogger()
    executive = ExecutiveManager(
        orchestrator_service=ExecutiveOrchestrator(pipeline=pipeline),
        logger_service=logger,
    )
    kernel = Kernel(
        configuration=create_configuration(tmp_path / "runtime"),
        executive=executive,
    )
    objective = objectives.create("isolated runtime objective")

    result = kernel.execute_objective(objective)

    assert result.completed is True
    assert result.classification == "analyze_objective"
    assert result.assignment is member
    assert result.execution_report.success is True
    assert result.reflection.objective is objective
    assert len(result.plan.tasks) == 5
    assert all(task.status == "completed" for task in result.plan.tasks)
    assert len(queue.items()) == 6
    assert all(item.status == "completed" for item in queue.items())
    assert len(stores.plan_db.load()) == 1
    assert len(stores.queue_db.load()) == 6
    assert len(stores.reflection_db.load()) == 1
    assert len(stores.memory_db.load()) == 1
    assert len(stores.knowledge_db.load()) == 1
    assert objective.status == "pending"
    assert logger.messages == [
        "Executive executing 'isolated runtime objective'",
        "Executive execution complete.",
    ]
