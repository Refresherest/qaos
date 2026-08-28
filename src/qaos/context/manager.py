"""
QAOS Context Manager
"""

from .context import Context
from .registry import ContextRegistry, context_registry

from qaos.retrieval import retrieval_manager


class ContextManager:

    def __init__(self, retrieval=None, registry=None):
        uses_default_retrieval = retrieval is None
        self._retrieval = (
            retrieval_manager if uses_default_retrieval else retrieval
        )
        self._registry = registry or (
            context_registry
            if uses_default_retrieval
            else ContextRegistry()
        )

    def create(self, objective):

        context = Context(objective)

        results = self._retrieval.search(
            objective.goal
        )

        # -------------------------
        # Memory
        # -------------------------

        for memory in results["memory"]:

            context.add_memory(memory)

        # -------------------------
        # Knowledge
        # -------------------------

        for knowledge in results["knowledge"]:

            context.add_knowledge(
                knowledge
            )

        # -------------------------
        # Artifacts
        # -------------------------

        for artifact in results["artifacts"]:

            context.add_artifact(
                artifact
            )

        self._registry.register(context)

        return context

    def get(self, objective):

        return self._registry.get(objective)

    def contexts(self):

        return self._registry.all()


context_manager = ContextManager()
