"""
QAOS Knowledge Manager
"""

from qaos.storage import create_stores, DATA

from .knowledge import Knowledge
from .registry import KnowledgeRegistry, knowledge_registry


class KnowledgeManager:

    def __init__(self, stores=None, registry=None):

        uses_default_stores = stores is None
        self._stores = stores or create_stores(DATA)
        self._registry = registry or (
            knowledge_registry
            if uses_default_stores
            else KnowledgeRegistry()
        )

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

            self._registry.register(knowledge)

    # ---------------------------------

    def _save(self):

        data = []

        for knowledge in self._registry.all().values():

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

        self._registry.register(knowledge)

        self._save()

        return knowledge

    # ---------------------------------

    def get(self, title):

        return self._registry.get(title)

    def knowledge(self):

        return self._registry.all()

    def reload(self):

        self._registry.all().clear()

        self._load()


knowledge_manager = KnowledgeManager()
