"""
QAOS Skill
"""

from qaos.capabilities import capability_manager


class Skill:

    def __init__(
        self,
        name,
        capability,
        capabilities=None,
    ):

        self.name = name
        self.capability = capability
        self._capabilities = (
            capability_manager if capabilities is None else capabilities
        )

    # ---------------------------------

    def execute(self, item):

        print(
            f"[Skill:{self.name}] "
            f"Executing '{item.objective}'"
        )

        capability = self._capabilities.get(
            self.capability
        )

        if capability is None:

            raise RuntimeError(
                f"Capability '{self.capability}' "
                f"not registered."
            )

        return capability.execute(item)

    # ---------------------------------

    def __repr__(self):

        return (
            f"<Skill {self.name}>"
        )
