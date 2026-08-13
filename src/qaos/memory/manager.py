"""
QAOS Memory Manager
"""

from qaos.storage import create_stores, DATA

from .memory import Memory
from .registry import (
    register,
    unregister,
    get,
    all,
)


class MemoryManager:

    def __init__(self, stores=None):

        self._stores = stores or create_stores(DATA)

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

            register(memory)

    # ---------------------------------

    def _save(self):

        data = []

        for memory in all().values():

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

        register(memory)

        self._save()

        return memory

    # ---------------------------------

    def register(self, memory):

        register(memory)

        self._save()

    # ---------------------------------

    def unregister(self, title):

        unregister(title)

        self._save()

    # ---------------------------------

    def get(self, title):

        return get(title)

    # ---------------------------------

    def memories(self):

        return all()

    # ---------------------------------

    def save(self):

        self._save()

    # ---------------------------------

    def reload(self):

        self._load()


memory_manager = MemoryManager()