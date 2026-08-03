"""
QAOS Capability Registry
"""

CAPABILITIES = {}


def register(capability):
    CAPABILITIES[capability.name] = capability


def unregister(name):
    CAPABILITIES.pop(name, None)


def get(name):
    return CAPABILITIES.get(name)


def all():
    return CAPABILITIES