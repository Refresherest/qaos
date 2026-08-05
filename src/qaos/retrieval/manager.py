"""
QAOS Retrieval Manager
"""

from .engine import retrieval_engine


class RetrievalManager:

    def search(self, query):

        return retrieval_engine.search(
            query
        )


retrieval_manager = RetrievalManager()