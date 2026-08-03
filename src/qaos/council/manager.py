"""
QAOS Executive Council Manager
"""

from .registry import get, all


class CouncilManager:

    def members(self):
        return all()

    def execute(self, name):
        member = get(name)

        if member is None:
            raise ValueError(
                f"Unknown council member: {name}"
            )

        member.run()

    def initialize(self):
        for member in all().values():
            member.initialize()

    def shutdown(self):
        for member in all().values():
            member.shutdown()


council_manager = CouncilManager()