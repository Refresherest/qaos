"""
QAOS Memory Manager
"""

from qaos.memory.registry import (
    register,
    unregister,
    get,
    all_memories,
)


class MemoryManager:

    def register(self, memory):
        register(memory)

    def unregister(self, name):
        unregister(name)

    def get(self, name):
        return get(name)

    def memories(self):
        return all_memories()

    def initialize(self):
        for memory in all_memories().values():
            memory.initialize()

    def shutdown(self):
        for memory in all_memories().values():
            memory.shutdown()


memory_manager = MemoryManager()