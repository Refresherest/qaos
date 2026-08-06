"""
QAOS Context
"""


class Context:

    def __init__(self, objective):

        self.objective = objective

        self.reasoning = None

        self.executive = None

        self.notes = []

        self.memory = []

        self.knowledge = []

        self.artifacts = []

        self.executives = []

        self.metadata = {}

    # -------------------------
    # Reasoning
    # -------------------------

    def set_reasoning(self, reasoning):

        self.reasoning = reasoning

    # -------------------------
    # Executive
    # -------------------------

    def set_executive(self, executive):

        self.executive = executive

        if (
            executive is not None
            and executive not in self.executives
        ):

            self.executives.append(
                executive
            )

    def add_executive(self, executive):

        if (
            executive is not None
            and executive not in self.executives
        ):

            self.executives.append(
                executive
            )

    # -------------------------
    # Briefing Notes
    # -------------------------

    def add_note(self, note):

        self.notes.append(note)

    # -------------------------
    # Memory
    # -------------------------

    def add_memory(self, memory):

        self.memory.append(memory)

    # -------------------------
    # Knowledge
    # -------------------------

    def add_knowledge(self, knowledge):

        self.knowledge.append(
            knowledge
        )

    # -------------------------
    # Artifacts
    # -------------------------

    def add_artifact(self, artifact):

        self.artifacts.append(
            artifact
        )

    # -------------------------
    # Metadata
    # -------------------------

    def set(self, key, value):

        self.metadata[key] = value

    def get(
        self,
        key,
        default=None,
    ):

        return self.metadata.get(
            key,
            default,
        )

    # -------------------------
    # Summary
    # -------------------------

    def summary(self):

        return {

            "objective": self.objective.goal,

            "reasoning": self.reasoning,

            "executive": (
                self.executive.title
                if self.executive
                else None
            ),

            "notes": len(self.notes),

            "memory": len(self.memory),

            "knowledge": len(self.knowledge),

            "artifacts": len(self.artifacts),

            "executives": len(self.executives),

            "metadata": self.metadata,
        }

    def __repr__(self):

        return (
            f"<Context {self.objective.goal}>"
        )