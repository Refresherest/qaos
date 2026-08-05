"""
QAOS Context Manager
"""

from .context import Context
from .registry import (
    register,
    get,
    all,
)

from qaos.retrieval import retrieval_manager


class ContextManager:

    def create(self, objective):

        context = Context(objective)

        results = retrieval_manager.search(
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

        register(context)

        return context

    def get(self, objective):

        return get(objective)

    def contexts(self):

        return all()


context_manager = ContextManager()