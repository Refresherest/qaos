"""
QAOS Plan Generator
"""

from qaos.reasoning import reasoning_engine
from qaos.briefing import briefing_manager
from qaos.executive import executive_manager
from qaos.skills import get as get_skill
from qaos.actions import action_manager

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

        plan = Plan(
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

            for skill_name in executive.skills():

                briefing.add(
                    executive.title,
                    f"Capability: {skill_name}",
                )

                skill = get_skill(
                    skill_name
                )

                if skill:

                    actions = skill.actions(
                        objective.goal
                    )

                    for action in actions:

                        plan.add_task(
                            action.description,
                            executive.title,
                            lambda a=action: (
                                action_manager.execute(a)
                            ),
                        )

        for note in briefing.notes:

            plan.add_task(
                f"Review: {note['author']}",
                note["author"],
                lambda text=note["note"]: print(
                    text
                ),
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