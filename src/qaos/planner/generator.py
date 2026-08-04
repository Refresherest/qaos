"""
QAOS Plan Generator
"""

from qaos.reasoning import reasoning_engine
from qaos.briefing import briefing_manager
from qaos.executive import executive_manager

from .plan import Plan


class PlanGenerator:

    def generate(self, objective):

        briefing = briefing_manager.create(
            objective
        )

        analysis = reasoning_engine.think(
            objective
        )

        briefing.add(
            "Reasoning Engine",
            analysis["analysis"],
        )

        executive = executive_manager.resolve(
            objective.goal
        )

        if executive:

            briefing.add(
                executive.title,
                (
                    f"Objective assigned to "
                    f"{executive.title}"
                ),
            )

            for skill in executive.skills():

                briefing.add(
                    executive.title,
                    f"Capability: {skill}",
                )

        plan = Plan(objective.goal)

        for note in briefing.notes:

            plan.add_task(
                f"Review: {note['author']}",
                note["author"],
                lambda text=note["note"]: print(text),
            )

        plan.add_task(
            "Execute objective",
            "Execution Engine",
            lambda: print(
                "Execution complete."
            ),
        )

        return plan


plan_generator = PlanGenerator()