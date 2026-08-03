"""
QAOS Executive Council Manager
"""

from .registry import get


class CouncilManager:

    def execute(self, name):
        member = get(name)

        if member is None:
            raise ValueError(
                f"Unknown council member: {name}"
            )

        return member.run()

    def members(self):
        from .registry import all

        return all()


council_manager = CouncilManager()