"""
QAOS Reasoning Engine
"""


class ReasoningEngine:

    def think(self, context):

        objective = context.objective

        print(
            f"[Reasoning] Thinking about: "
            f"{objective.goal}"
        )

        return {
            "analysis": (
                f"Objective requires planning: "
                f"{objective.goal}"
            ),
            "confidence": 1.0,
        }


reasoning_engine = ReasoningEngine()