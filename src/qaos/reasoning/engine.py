"""
QAOS Reasoning Engine
"""


class ReasoningEngine:
    """
    Produces structured reasoning for objectives.

    Currently rule-based.

    Later this becomes the LLM interface.
    """

    def think(self, objective):

        print(
            f"[Reasoning] Thinking about: "
            f"{objective.goal}"
        )

        return {
            "analysis": (
                f"Objective requires planning: "
                f"{objective.goal}"
            )
        }


reasoning_engine = ReasoningEngine()