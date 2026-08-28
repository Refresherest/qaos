"""
QAOS Plan Manager
"""

from qaos.storage import create_stores, DATA

from .plan import Plan
from .task import Task
from .registry import PlanRegistry, plan_registry

from .generator import plan_generator


class PlannerManager:

    def __init__(self, stores=None, registry=None):

        uses_default_stores = stores is None

        self._stores = stores or create_stores(DATA)
        self._registry = registry or (
            plan_registry
            if uses_default_stores
            else PlanRegistry()
        )

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

            self._registry.register(plan)

    # ---------------------------------

    def _save(self):

        data = []

        for plan in self._registry.all().values():

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

        self._registry.register(plan)

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

        self._registry.register(plan)

        self._save()

    # ---------------------------------

    def unregister(self, objective):

        self._registry.unregister(objective)

        self._save()

    # ---------------------------------

    def get(self, objective):

        return self._registry.get(objective)

    # ---------------------------------

    def plans(self):

        return self._registry.all()

    # ---------------------------------

    def save(self):

        self._save()


planner_manager = PlannerManager()
