"""
QAOS Memory Manager
"""

from qaos.memory.memory import memory


class MemoryManager:

    def set(self, key, value):
        memory.set(key, value)

    def get(self, key, default=None):
        return memory.get(key, default)

    def delete(self, key):
        memory.delete(key)

    def clear(self):
        memory.clear()

    def all(self):
        return memory.all()


memory_manager = MemoryManager()