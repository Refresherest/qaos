"""
QAOS Persistence Base Class
"""


class Persistence:

    name = "persistence"

    def initialize(self):
        print(f"[Persistence] Initializing {self.name}")

    def shutdown(self):
        print(f"[Persistence] Shutting down {self.name}")

    def load(self):
        raise NotImplementedError

    def save(self):
        raise NotImplementedError