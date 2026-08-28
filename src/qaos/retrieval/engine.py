"""
QAOS Retrieval Engine
"""

from qaos.memory import memory_manager
from qaos.knowledge import knowledge_manager
from qaos.artifacts import artifact_manager


class RetrievalEngine:

    def __init__(
        self,
        *,
        memory=None,
        knowledge=None,
        artifacts=None,
    ):
        self._memory = memory_manager if memory is None else memory
        self._knowledge = knowledge_manager if knowledge is None else knowledge
        self._artifacts = artifact_manager if artifacts is None else artifacts

    def search(self, query):

        results = {
            "memory": [],
            "knowledge": [],
            "artifacts": [],
        }

        query = query.lower()

        # -------------------------
        # Search Memory
        # -------------------------

        for memory in self._memory.memories().values():

            text = str(memory).lower()

            if query in text:
                results["memory"].append(memory)

        # -------------------------
        # Search Knowledge
        # -------------------------

        for knowledge in self._knowledge.knowledge().values():

            text = (
                knowledge.title
                + " "
                + knowledge.content
            ).lower()

            if query in text:
                results["knowledge"].append(
                    knowledge
                )

        # -------------------------
        # Search Artifacts
        # -------------------------

        for artifact in self._artifacts.artifacts().values():

            text = (
                artifact.title
                + " "
                + artifact.content
            ).lower()

            if query in text:
                results["artifacts"].append(
                    artifact
                )

        return results


retrieval_engine = RetrievalEngine()
