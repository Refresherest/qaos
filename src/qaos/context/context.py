"""
QAOS Context
"""


class Context:

    def __init__(self, objective):

        self.objective = objective

        self.memory = []

        self.knowledge = []

        self.artifacts = []

        self.executives = []

        self.metadata = {}

    # -------------------------
    # Memory
    # -------------------------

    def add_memory(self, memory):

        self.memory.append(memory)

    # -------------------------
    # Knowledge
    # -------------------------

    def add_knowledge(self, knowledge):

        self.knowledge.append(knowledge)

    # -------------------------
    # Artifacts
    # -------------------------

    def add_artifact(self, artifact):

        self.artifacts.append(artifact)

    # -------------------------
    # Executives
    # -------------------------

    def add_executive(self, executive):

        self.executives.append(executive)

    # -------------------------
    # Metadata
    # -------------------------

    def set(self, key, value):

        self.metadata[key] = value

    def get(self, key, default=None):

        return self.metadata.get(
            key,
            default,
        )

    def __repr__(self):

        return (
            f"<Context {self.objective.goal}>"
        )