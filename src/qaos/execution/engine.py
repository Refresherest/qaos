"""
QAOS Execution Engine
"""

from qaos.queue import (
    QueueItem,
    queue_manager,
)

from qaos.planner import planner_manager
from qaos.reflection import reflection_manager

from .report import ExecutionReport


class ExecutionEngine:
    """
    Executes an Objective and produces an
    ExecutionReport describing everything that
    happened during execution.
    """

    def execute(self, objective):

        report = ExecutionReport(objective)

        try:

            print("=" * 50)
            print("QAOS Execution Engine")
            print("=" * 50)
            print()

            print(
                f"Objective : {objective.goal}"
            )

            #
            # Obtain (or generate) the plan
            #

            plan = planner_manager.get(
                objective.goal
            )

            if plan is None:

                plan = planner_manager.plan(
                    objective
                )

            report.plan = plan

            #
            # Queue every incomplete task
            #

            for task in plan.tasks:

                report.tasks.append(task)

                if task.status == "completed":
                    continue

                item = QueueItem(
                    objective=objective.goal,
                    assignee="default",
                    action=task,
                )

                queue_manager.add(item)

            report.worker = "default"

            #
            # Execute queued work
            #

            queue_manager.process()

            #
            # Persist planner state
            #

            planner_manager.save()

            #
            # Reflection
            #

            reflection = reflection_manager.create(

                objective=objective,

                summary="Objective completed.",

                successes=[
                    "Objective completed successfully."
                ],

                failures=[],

            )

            report.reflection = reflection

            report.complete()

        except Exception as e:

            report.fail(e)

            raise

        return report


execution_engine = ExecutionEngine()