"""
QAOS Council Router
"""


class CouncilRouter:

    def route(self, task):

        description = task.description.lower()

        if "analyse" in description:
            return "cto"

        if "design" in description:
            return "cto"

        if "implement" in description:
            return "cto"

        if "validate" in description:
            return "cto"

        if "reflection" in description:
            return "cos"

        return "cos"


council_router = CouncilRouter()