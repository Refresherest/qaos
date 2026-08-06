"""
QAOS Agent
"""

from qaos.skills import skill_resolver


class Agent:

    def __init__(self, name):

        self.name = name

    # ---------------------------------

    def execute(self, item):

        print(
            f"[Agent:{self.name}] "
            f"Processing '{item.objective}'"
        )

        #
        # Resolve Skill
        #

        skill = skill_resolver.resolve(
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