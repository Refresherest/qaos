"""
QAOS Memory Registry
"""

MEMORIES = {}


def register(memory):
    MEMORIES[memory.name] = memory


def unregister(name):
    MEMORIES.pop(name, None)


def get(name):
    return MEMORIES.get(name)


def all_memories():
    return MEMORIES