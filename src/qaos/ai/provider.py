"""
QAOS AI Provider Base Class
"""


class AIProvider:

    name = "base"
    test_only = False

    def initialize(self):
        print(f"[AI] Initializing {self.name}")

    def generate(self, prompt: str) -> str:
        raise NotImplementedError(
            "AI providers must implement generate()."
        )

    def shutdown(self):
        print(f"[AI] Shutting down {self.name}")
