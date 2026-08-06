"""
QAOS Capability Manager
"""

from .registry import (
    register,
    unregister,
    get,
    all,
)


class CapabilityManager:
    """
    Central manager for QAOS capabilities.
    """

    # ----------------------------------

    def register(self, capability):
        """
        Register a capability.
        """

        register(capability)

    # ----------------------------------

    def unregister(self, name):
        """
        Remove a capability.
        """

        unregister(name)

    # ----------------------------------

    def get(self, name):
        """
        Return a capability.
        """

        return get(name)

    # ----------------------------------

    def capabilities(self):
        """
        Return all registered capabilities.
        """

        return all()

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