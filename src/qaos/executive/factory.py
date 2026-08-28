"""Provider-neutral construction of the operational Executive graph."""

from qaos.agents import Agent
from qaos.agents.manager import AgentManager
from qaos.agents.registry import AgentRegistry
from qaos.artifacts.manager import ArtifactManager
from qaos.capabilities.manager import CapabilityManager
from qaos.capabilities.registry import CapabilityRegistry
from qaos.capabilities.system import SystemCapability
from qaos.classifier.manager import ClassifierManager
from qaos.classifier.registry import create_default_classifier
from qaos.context.manager import ContextManager
from qaos.council.chief_of_staff import ChiefOfStaff
from qaos.council.chief_technology_officer import ChiefTechnologyOfficer
from qaos.council.delegator import Delegator
from qaos.council.manager import CouncilManager
from qaos.council.registry import CouncilRegistry
from qaos.execution.engine import ExecutionEngine
from qaos.execution.manager import ExecutionManager
from qaos.execution.registry import ExecutionRegistry
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
from qaos.workers.default import DefaultWorker
from qaos.workers.manager import WorkerManager
from qaos.workers.registry import WorkerRegistry

from .manager import ExecutiveManager
from .orchestrator import ExecutiveOrchestrator
from .pipeline import ExecutivePipeline


def create_executive(stores, *, objectives=None, logger=None):
    """Create an isolated ExecutiveManager bound to one Stores workspace.

    Pass an ObjectiveManager through ``objectives`` when the caller creates
    objectives and requires that same registry to own lifecycle persistence.
    """
    memory = MemoryManager(stores=stores)
    knowledge = KnowledgeManager(stores=stores)
    artifacts = ArtifactManager(stores=stores)
    objective_manager = (
        ObjectiveManager(stores=stores) if objectives is None else objectives
    )

    capabilities = CapabilityManager(registry=CapabilityRegistry())
    capabilities.register(SystemCapability())
    skills = SkillRegistry()
    SkillManager(registry=skills).register(
        Skill("planning", "system", capabilities=capabilities)
    )
    agents = AgentManager(registry=AgentRegistry())
    agents.register(Agent("default", resolver=SkillResolver(registry=skills)))
    queue = QueueManager(
        stores=stores,
        workers=WorkerManager(
            registry=WorkerRegistry(),
            default=DefaultWorker(agents=agents),
        ),
    )

    council_registry = CouncilRegistry()
    ChiefOfStaff(registry=council_registry)
    ChiefTechnologyOfficer(registry=council_registry)
    council = CouncilManager(
        registry=council_registry,
        delegator_service=Delegator(
            registry=council_registry,
            objectives=objective_manager,
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

    pipeline = ExecutivePipeline(
        classifier=ClassifierManager(
            classifier_service=create_default_classifier()
        ),
        council=council,
        planner=planner,
        execution=ExecutionManager(
            registry=execution_registry,
            objectives=objective_manager,
        ),
        reflection=ReflectionManager(stores=stores),
        learning=LearningManager(
            learner_service=Learner(
                engine=LearningEngine(memory=memory, knowledge=knowledge)
            )
        ),
    )

    return ExecutiveManager(
        orchestrator_service=ExecutiveOrchestrator(pipeline=pipeline),
        logger_service=logger,
    )
