"""
QAOS Skill
"""

from qaos.capabilities import capability_manager


class Skill:

    def __init__(
        self,
        name,
        capability,
    ):

        self.name = name
        self.capability = capability

    # ---------------------------------

    def execute(self, item):

        print(
            f"[Skill:{self.name}] "
            f"Executing '{item.objective}'"
        )

        capability = capability_manager.get(
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