"""
QAOS Retrieval Engine
"""

from qaos.memory import memory_manager
from qaos.knowledge import knowledge_manager
from qaos.artifacts import artifact_manager


class RetrievalEngine:

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

        for memory in memory_manager.memories().values():

            text = str(memory).lower()

            if query in text:
                results["memory"].append(memory)

        # -------------------------
        # Search Knowledge
        # -------------------------

        for knowledge in knowledge_manager.knowledge().values():

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

        for artifact in artifact_manager.artifacts().values():

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