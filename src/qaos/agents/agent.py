"""
QAOS Agent
"""

from qaos.skills import skill_resolver


class Agent:

    def __init__(self, name, resolver=None):

        self.name = name
        self._resolver = skill_resolver if resolver is None else resolver

    # ---------------------------------

    def execute(self, item):

        print(
            f"[Agent:{self.name}] "
            f"Processing '{item.objective}'"
        )

        #
        # Resolve Skill
        #

        skill = self._resolver.resolve(
            item
        )

        #
        # Delegate execution
        #

        return skill.execute(item)

    # ---------------------------------

    def __repr__(self):

        return (
            f"<Agent {self.name}>"
        )
