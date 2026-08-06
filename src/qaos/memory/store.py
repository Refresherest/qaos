"""
QAOS Memory Store
"""


class MemoryStore:

    def __init__(self):

        self._items = []

    def add(self, memory):

        self._items.append(memory)

    def remove(self, memory):

        if memory in self._items:

            self._items.remove(memory)

    def clear(self):

        self._items.clear()

    def items(self):

        return self._items

    def all(self):

        return self._items