"""
QAOS Execution Engine
"""

from qaos.queue import (
    QueueItem,
    queue_manager,
)

from qaos.planner import planner_manager
from .report import ExecutionReport


class ExecutionEngine:
    """
    Executes an Objective and produces an
    ExecutionReport describing everything that
    happened during execution.
    """

    def __init__(self, *, planner=None, queue=None):
        self._planner = planner_manager if planner is None else planner
        self._queue = queue_manager if queue is None else queue

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

            plan = self._planner.get(
                objective.goal
            )

            if plan is None:

                plan = self._planner.plan(
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

                self._queue.add(item)

            report.worker = "default"

            #
            # Execute queued work
            #

            self._queue.process()

            #
            # Persist planner state
            #

            self._planner.save()

            report.complete()

        except Exception as e:

            report.fail(e)

            raise

        return report


execution_engine = ExecutionEngine()
