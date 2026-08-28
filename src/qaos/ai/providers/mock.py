"""
QAOS Mock AI Provider
"""

from qaos.ai.provider import AIProvider


class MockProvider(AIProvider):
    """
    Mock provider used for testing the AI engine.
    """

    name = "mock"

    def generate(self, prompt: str):
        return f"[MOCK AI] Response to: {prompt}"
