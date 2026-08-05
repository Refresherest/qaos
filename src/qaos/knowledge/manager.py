"""
QAOS Knowledge Manager
"""

from .registry import (
    register,
    get,
    all,
)


class KnowledgeManager:

    def create(

        self,
        title,
        category,
        content,
        source=None,
        tags=None,

    ):

        from .knowledge import Knowledge

        knowledge = Knowledge(
            title=title,
            category=category,
            content=content,
            source=source,
            tags=tags,
        )

        register(knowledge)

        return knowledge

    def get(self, title):

        return get(title)

    def knowledge(self):

        return all()


knowledge_manager = KnowledgeManager()