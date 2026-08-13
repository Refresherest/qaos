"""
QAOS Plan Manager
"""

from qaos.storage import create_stores, DATA

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

    def __init__(self, stores=None):

        self._stores = stores or create_stores(DATA)

        self._load()

    # ---------------------------------

    def _load(self):

        for item in self._stores.plan_db.load():

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

        self._stores.plan_db.save(data)

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