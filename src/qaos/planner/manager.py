"""
QAOS Plan Manager
"""

from uuid import uuid4

from qaos.storage import create_stores, DATA

from .plan import Plan
from .task import Task
from .registry import PlanRegistry, plan_registry

from .generator import plan_generator


class PlannerManager:

    def __init__(
        self,
        stores=None,
        registry=None,
        generator=None,
        task_id_generator=None,
    ):

        uses_default_stores = stores is None

        self._stores = stores or create_stores(DATA)
        self._registry = registry or (
            plan_registry
            if uses_default_stores
            else PlanRegistry()
        )
        self._generator = plan_generator if generator is None else generator
        self._task_id_generator = task_id_generator or (lambda: str(uuid4()))
        self._legacy_tasks = set()

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

                task = Task.from_dict(task_data)
                plan.tasks.append(task)

                if task.task_id is None:
                    self._legacy_tasks.add(task)

            self._registry.register(plan)

        self._validate_task_identities()

    # ---------------------------------

    def _save(self):

        self._prepare_task_identities()

        data = []

        for plan in self._registry.records():

            data.append(plan.to_dict())

        self._stores.plan_db.save(data)

    # ---------------------------------

    def _prepare_task_identities(self):
        seen = self._identified_tasks()

        for plan in self._registry.records():
            for task in plan.tasks:
                if task.task_id is not None or task in self._legacy_tasks:
                    continue

                task_id = self._task_id_generator()
                if task_id in seen:
                    raise ValueError(f"duplicate task_id: {task_id}")

                task._assign_identity(task_id)
                seen[task_id] = task

    # ---------------------------------

    def _identified_tasks(self):
        seen = {}

        for plan in self._registry.records():
            for task in plan.tasks:
                if task.task_id is None:
                    continue

                existing = seen.get(task.task_id)
                if existing is not None and existing is not task:
                    raise ValueError(f"duplicate task_id: {task.task_id}")

                seen[task.task_id] = task

        return seen

    # ---------------------------------

    def _validate_task_identities(self):
        self._identified_tasks()

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

    def prepare_tasks(self, plan):

        if plan not in self._registry.records():
            raise ValueError("plan must be registered before Task preparation")

        self._prepare_task_identities()

    # ---------------------------------

    def save(self):

        self._save()


planner_manager = PlannerManager()
