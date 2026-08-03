"""
QAOS Capability Manager
"""

from qaos.capabilities.registry import (
    register,
    unregister,
    get,
    all,
)


class CapabilityManager:

    def register(self, capability):
        register(capability)

    def unregister(self, name):
        unregister(name)

    def get(self, name):
        return get(name)

    def capabilities(self):
        return all()

    def initialize(self):
        for capability in all().values():
            capability.initialize()

    def shutdown(self):
        for capability in all().values():
            capability.shutdown()

    def execute(self, name, *args, **kwargs):
        capability = get(name)

        if capability is None:
            raise ValueError(
                f"Unknown capability: {name}"
            )

        return capability.execute(*args, **kwargs)


capability_manager = CapabilityManager()