"""
QAOS AI Engine
"""

from qaos.ai.registry import get
from qaos.ai.generation import GenerationEvidence


class AIEngine:
    """
    Central AI execution engine.
    """

    def __init__(self, provider=None):
        self._injected_provider = provider
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
        self._injected_provider = None

    def provider(self):
        """
        Return the active provider.
        """

        if self._injected_provider is not None:
            return self._injected_provider

        return get(self._provider)

    def generate(self, prompt: str):
        """
        Generate a response using the active provider.
        """

        return self.generate_with_evidence(prompt).output

    def generate_with_evidence(self, prompt: str) -> GenerationEvidence:
        """Generate once and return the exact prompt/output as evidence."""

        provider = self.provider()

        if provider is None:
            raise ValueError(
                f"No active AI provider: {self._provider}"
            )

        output = provider.generate(prompt)

        return GenerationEvidence(
            prompt=prompt,
            output=output,
        )


engine = AIEngine()
