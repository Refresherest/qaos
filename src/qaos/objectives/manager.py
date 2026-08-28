"""
QAOS Objective Manager
"""

from qaos.storage import create_stores, DATA

from .objective import Objective
from .registry import ObjectiveRegistry, objective_registry


class ObjectiveManager:

    def __init__(self, stores=None, registry=None):

        uses_default_stores = stores is None

        self._stores = stores or create_stores(DATA)
        self._registry = registry or (
            objective_registry
            if uses_default_stores
            else ObjectiveRegistry()
        )

        self._load()

    # ---------------------------------

    def _load(self):

        for item in self._stores.objective_db.load():

            objective = Objective(
                item["goal"]
            )

            objective.status = item.get(
                "status",
                "pending",
            )

            objective.created = item.get("created")
            objective.started = item.get("started")
            objective.completed = item.get("completed")

            self._registry.register(objective)

    # ---------------------------------

    def _save(self):

        data = []

        for objective in self._registry.all().values():

            data.append({

                "goal": objective.goal,

                "status": objective.status,

                "created": objective.created,

                "started": objective.started,

                "completed": objective.completed,

            })

        self._stores.objective_db.save(data)

    # ---------------------------------
    # Public save API
    # ---------------------------------

    def save(self):

        self._save()

    # ---------------------------------

    def create(self, goal):

        objective = Objective(goal)

        self._registry.register(objective)

        self._save()

        return objective

    # ---------------------------------

    def register(self, objective):

        self._registry.register(objective)

        self._save()

    # ---------------------------------

    def unregister(self, goal):

        self._registry.unregister(goal)

        self._save()

    # ---------------------------------

    def get(self, goal):

        return self._registry.get(goal)

    # ---------------------------------

    def objectives(self):

        return self._registry.all()

    # ---------------------------------

    def assign(self, objective, member):

        objective.assign(member)
        self._save()

    # ---------------------------------

    def assign_plan(self, objective, plan):

        objective.assign_plan(plan)
        self._save()

    # ---------------------------------

    def start(self, objective):

        objective.start()
        self._save()

    # ---------------------------------

    def complete(self, objective):

        objective.complete()
        self._save()

    # ---------------------------------

    def fail(self, objective):

        objective.fail()
        self._save()


objective_manager = ObjectiveManager()
