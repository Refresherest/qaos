"""
QAOS Capability Registry
"""

class CapabilityRegistry:
    """Registry state owned by one capability-manager lifecycle."""

    def __init__(self):
        self._capabilities = {}

    def register(self, capability):
        self._capabilities[capability.name] = capability

    def unregister(self, name):
        self._capabilities.pop(name, None)

    def get(self, name):
        return self._capabilities.get(name)

    def all(self):
        return dict(self._capabilities)

    def clear(self):
        self._capabilities.clear()


capability_registry = CapabilityRegistry()


def register(capability):
    """
    Register a capability.
    """

    capability_registry.register(capability)


# ----------------------------------


def unregister(name):
    """
    Remove a capability.
    """

    capability_registry.unregister(name)


# ----------------------------------


def get(name):
    """
    Return a capability.
    """

    return capability_registry.get(name)


# ----------------------------------


def all():
    """
    Return all capabilities.
    """

    return capability_registry.all()


# ----------------------------------


def clear():
    """
    Remove every registered capability.
    """

    capability_registry.clear()
