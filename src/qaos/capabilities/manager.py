"""
QAOS Capability Manager
"""

from .registry import capability_registry


class CapabilityManager:
    """
    Central manager for QAOS capabilities.
    """

    def __init__(self, registry=None):
        self._registry = (
            capability_registry if registry is None else registry
        )

    # ----------------------------------

    def register(self, capability):
        """
        Register a capability.
        """

        self._registry.register(capability)

    # ----------------------------------

    def unregister(self, name):
        """
        Remove a capability.
        """

        self._registry.unregister(name)

    # ----------------------------------

    def get(self, name):
        """
        Return a capability.
        """

        return self._registry.get(name)

    # ----------------------------------

    def capabilities(self):
        """
        Return all registered capabilities.
        """

        return self._registry.all()

    # ----------------------------------

    def execute(
        self,
        capability,
        operation,
        *args,
        **kwargs,
    ):
        """
        Execute an operation on a capability.
        """

        instance = self.get(
            capability
        )

        if instance is None:

            raise RuntimeError(
                f"Capability '{capability}' not found."
            )

        return instance.execute(
            operation,
            *args,
            **kwargs,
        )


capability_manager = CapabilityManager()
