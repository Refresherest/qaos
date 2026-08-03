"""
QAOS AI Engine
"""

from qaos.ai.registry import get


class AIEngine:
    """
    Central AI execution engine.
    """

    def generate(self, provider_name: str, prompt: str):
        provider = get(provider_name)

        if provider is None:
            raise ValueError(
                f"Unknown AI provider: {provider_name}"
            )

        return provider.generate(prompt)


engine = AIEngine()