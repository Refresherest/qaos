"""
QAOS Plan Manager
"""

from qaos.storage import plan_db

from .plan import Plan
from .task import Task
from .registry import (
    register,
    unregister,
    get,
    all,
)

from .generator import plan_generator


class PlannerManager:

    def __init__(self):

        self._load()

    # ---------------------------------

    def _load(self):

        for item in plan_db.load():

            plan = Plan(
                item["objective"]
            )

            for task_data in item.get(
                "tasks",
                [],
            ):

                plan.tasks.append(
                    Task.from_dict(
                        task_data
                    )
                )

            register(plan)

    # ---------------------------------

    def _save(self):

        data = []

        for plan in all().values():

            objective = plan.objective

            if hasattr(
                objective,
                "goal",
            ):
                objective = objective.goal

            data.append({

                "objective": objective,

                "tasks": [

                    task.to_dict()

                    for task in plan.tasks

                ],

            })

        plan_db.save(data)

    # ---------------------------------

    def create(self, objective):

        plan = Plan(
            objective
        )

        register(plan)

        self._save()

        return plan

    # ---------------------------------

    def plan(self, objective):

        return plan_generator.generate(
            self,
            objective,
        )

    # ---------------------------------

    def register(self, plan):

        register(plan)

        self._save()

    # ---------------------------------

    def unregister(self, objective):

        unregister(objective)

        self._save()

    # ---------------------------------

    def get(self, objective):

        return get(objective)

    # ---------------------------------

    def plans(self):

        return all()

    # ---------------------------------

    def save(self):

        self._save()


planner_manager = PlannerManager()