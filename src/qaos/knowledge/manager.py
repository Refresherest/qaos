"""
QAOS Knowledge Manager
"""

from qaos.storage import create_stores, DATA

from .knowledge import Knowledge
from .registry import (
    register,
    get,
    all,
)


class KnowledgeManager:

    def __init__(self, stores=None):

        self._stores = stores or create_stores(DATA)

        self._load()

    # ---------------------------------

    def _load(self):

        for item in self._stores.knowledge_db.load():

            knowledge = Knowledge(

                title=item["title"],
                category=item["category"],
                content=item["content"],
                source=item.get("source", ""),

            )

            register(knowledge)

    # ---------------------------------

    def _save(self):

        data = []

        for knowledge in all().values():

            data.append({

                "title": knowledge.title,
                "category": knowledge.category,
                "content": knowledge.content,
                "source": knowledge.source,

            })

        self._stores.knowledge_db.save(data)

    # ---------------------------------

    def create(

        self,
        title,
        category,
        content,
        source="",

    ):

        knowledge = Knowledge(

            title=title,
            category=category,
            content=content,
            source=source,

        )

        register(knowledge)

        self._save()

        return knowledge

    # ---------------------------------

    def get(self, title):

        return get(title)

    def knowledge(self):

        return all()

    def reload(self):

        all().clear()

        self._load()


knowledge_manager = KnowledgeManager()