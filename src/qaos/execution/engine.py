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

            plan = self._planner.get(objective)

            if plan is None:

                plan = self._planner.plan(
                    objective
                )

            report.plan = plan

            # Assign canonical Task identity before queueing when supported.
            prepare_tasks = getattr(self._planner, "prepare_tasks", None)
            if callable(prepare_tasks):
                prepare_tasks(plan)

            #
            # Queue every incomplete task
            #

            for task in plan.tasks:

                report.tasks.append(task)

                if task.status == "completed":
                    continue

                item = QueueItem(
                    objective=objective,
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

    def validate_recovery(self, objective):

        objective_id = getattr(objective, "objective_id", None)
        if not isinstance(objective_id, str) or not objective_id:
            raise ValueError("recovery requires an identified Objective")

        plan = self._planner.get_by_objective_id(objective_id)
        if plan is None or plan.objective_id != objective_id:
            raise ValueError("recovery requires a matching persisted Plan")

        targets = self._queue.validate_recovery(objective_id)
        pairs = []

        for item in targets:
            task = plan.get_task_by_id(item.task_id)
            if task is None:
                raise ValueError("recovery QueueItem Task is missing from Plan")
            if item.action is None or item.action.task_id != item.task_id:
                raise ValueError("recovery QueueItem action identity is inconsistent")
            if item.status != item.action.status or item.status != task.status:
                raise ValueError("Plan and Queue recovery statuses do not match")
            pairs.append((item, task))

        return plan, tuple(pairs)

    def recover(self, objective):

        _plan, pairs = self.validate_recovery(objective)
        canonical_tasks = {
            item.task_id: task
            for item, task in pairs
        }

        try:
            result = self._queue.recover(
                objective.objective_id,
                canonical_tasks,
            )
        except Exception:
            try:
                self._planner.save()
            except Exception:
                pass
            raise
        else:
            self._planner.save()
            return result


execution_engine = ExecutionEngine()
