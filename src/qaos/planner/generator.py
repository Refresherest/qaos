"""
QAOS Plan Generator
"""

from qaos.context import context_manager


class PlanGenerator:

    def generate(self, planner_manager, objective):

        context = context_manager.create(
            objective
        )

        plan = planner_manager.create(
            objective
        )

        # ---------------------------------

        if context.knowledge:

            plan.add_task(
                "Review existing knowledge"
            )

        if context.memory:

            plan.add_task(
                "Review previous experience"
            )

        if context.artifacts:

            plan.add_task(
                "Review existing artifacts"
            )

        # ---------------------------------

        plan.add_task(
            "Analyse objective"
        )

        plan.add_task(
            "Design solution"
        )

        plan.add_task(
            "Implement solution"
        )

        plan.add_task(
            "Validate implementation"
        )

        plan.add_task(
            "Generate reflection"
        )

        planner_manager.save()

        return plan


plan_generator = PlanGenerator()