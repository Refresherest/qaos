"""
QAOS Knowledge Registry
"""

class KnowledgeRegistry:
    """Registry state owned by one knowledge-manager lifecycle."""

    def __init__(self):
        self._registry = {}

    def register(self, knowledge):
        self._registry[knowledge.title] = knowledge

    def get(self, title):
        return self._registry.get(title)

    def all(self):
        return self._registry


knowledge_registry = KnowledgeRegistry()


def register(knowledge):
    knowledge_registry.register(knowledge)


def get(title):
    return knowledge_registry.get(title)


def all():
    return knowledge_registry.all()
