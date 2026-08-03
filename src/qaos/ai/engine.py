"""
QAOS AI Engine
"""

from qaos.ai.registry import get


class AIEngine:
    """
    Central AI execution engine.
    """

    def __init__(self):
        self._provider = "mock"

    def use(self, provider_name: str):
        """
        Switch the active AI provider.
        """

        if get(provider_name) is None:
            raise ValueError(
                f"Unknown AI provider: {provider_name}"
            )

        self._provider = provider_name

    def provider(self):
        """
        Return the active provider.
        """

        return get(self._provider)

    def generate(self, prompt: str):
        """
        Generate a response using the active provider.
        """

        provider = self.provider()

        if provider is None:
            raise ValueError(
                f"No active AI provider: {self._provider}"
            )

        return provider.generate(prompt)


engine = AIEngine()