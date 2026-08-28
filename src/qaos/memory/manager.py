"""
QAOS Memory Manager
"""

from qaos.storage import create_stores, DATA

from .memory import Memory
from .registry import MemoryRegistry, memory_registry


class MemoryManager:

    def __init__(self, stores=None, registry=None):

        uses_default_stores = stores is None

        self._stores = stores or create_stores(DATA)
        self._registry = registry or (
            memory_registry
            if uses_default_stores
            else MemoryRegistry()
        )

        self._load()

    # ---------------------------------

    def _load(self):

        for item in self._stores.memory_db.load():

            memory = Memory(
                item["title"],
                item["content"],
                item.get(
                    "category",
                    "general",
                ),
            )

            self._registry.register(memory)

    # ---------------------------------

    def _save(self):

        data = []

        for memory in self._registry.all().values():

            data.append({

                "title":
                    memory.title,

                "content":
                    memory.content,

                "category":
                    memory.category,

            })

        self._stores.memory_db.save(data)

    # ---------------------------------

    def create(
        self,
        title,
        content,
        category="general",
    ):

        memory = Memory(
            title,
            content,
            category,
        )

        self._registry.register(memory)

        self._save()

        return memory

    # ---------------------------------

    def register(self, memory):

        self._registry.register(memory)

        self._save()

    # ---------------------------------

    def unregister(self, title):

        self._registry.unregister(title)

        self._save()

    # ---------------------------------

    def get(self, title):

        return self._registry.get(title)

    # ---------------------------------

    def memories(self):

        return self._registry.all()

    # ---------------------------------

    def save(self):

        self._save()

    # ---------------------------------

    def reload(self):

        self._load()


memory_manager = MemoryManager()
