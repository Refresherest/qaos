"""
QAOS Plan Manager
"""

from qaos.storage import create_stores, DATA

from .plan import Plan
from .task import Task
from .registry import PlanRegistry, plan_registry

from .generator import plan_generator


class PlannerManager:

    def __init__(self, stores=None, registry=None, generator=None):

        uses_default_stores = stores is None

        self._stores = stores or create_stores(DATA)
        self._registry = registry or (
            plan_registry
            if uses_default_stores
            else PlanRegistry()
        )
        self._generator = plan_generator if generator is None else generator

        self._load()

    # ---------------------------------

    def _load(self):

        for item in self._stores.plan_db.load():

            plan = Plan(
                item["objective"],
                objective_id=item.get("objective_id"),
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

        for plan in self._registry.records():

            data.append(plan.to_dict())

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

        return self._generator.generate(
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

    def get_by_objective_id(self, objective_id):

        return self._registry.get_by_objective_id(objective_id)

    # ---------------------------------

    def plans(self):

        return self._registry.all()

    # ---------------------------------

    def plan_records(self):

        return self._registry.records()

    # ---------------------------------

    def save(self):

        self._save()


planner_manager = PlannerManager()
