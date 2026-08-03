"""
QAOS Memory Base Class
"""


class Memory:

    name = "memory"

    def initialize(self):
        print(f"[Memory] Initializing {self.name}")

    def shutdown(self):
        print(f"[Memory] Shutting down {self.name}")