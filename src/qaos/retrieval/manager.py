"""
QAOS Retrieval Manager
"""

from .engine import retrieval_engine


class RetrievalManager:

    def __init__(self, engine=None):
        self._engine = retrieval_engine if engine is None else engine

    def search(self, query):

        return self._engine.search(
            query
        )


retrieval_manager = RetrievalManager()
