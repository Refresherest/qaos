"""
QAOS Memory Registry
"""

class MemoryRegistry:
    """Registry state owned by one memory-manager lifecycle."""

    def __init__(self):
        self._registry = {}

    def register(self, memory):
        self._registry[memory.title] = memory

    def unregister(self, title):
        if hasattr(title, "title"):
            title = title.title

        self._registry.pop(title, None)

    def get(self, title):
        if hasattr(title, "title"):
            title = title.title

        return self._registry.get(title)

    def all(self):
        return self._registry


memory_registry = MemoryRegistry()


def register(memory):
    memory_registry.register(memory)


def unregister(title):
    memory_registry.unregister(title)


def get(title):
    return memory_registry.get(title)


def all():
    return memory_registry.all()
