"""
QAOS AI Provider Base Class
"""


class AIProvider:
    """
    Base class for all AI providers.
    """

    name = "base"

    def generate(self, prompt: str) -> str:
        raise NotImplementedError(
            "AI providers must implement generate()."
        )