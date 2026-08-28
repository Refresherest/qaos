"""
QAOS Executive Council Registry
"""

class CouncilRegistry:
    """Registry state owned by one council-manager lifecycle."""

    def __init__(self):
        self._members = {}

    def register(self, member):
        self._members[member.name] = member

    def get(self, name):
        return self._members.get(name)

    def all(self):
        return dict(self._members)


council_registry = CouncilRegistry()


def register(member):
    """
    Register an Executive Council member.
    """
    council_registry.register(member)


def get(name):
    """
    Return a council member.
    """
    return council_registry.get(name)


def all():
    """
    Return all registered members.
    """
    return council_registry.all()
