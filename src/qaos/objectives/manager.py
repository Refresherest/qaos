"""
QAOS Objective Manager
"""

from uuid import uuid4

from qaos.storage import create_stores, DATA

from .objective import Objective
from .registry import ObjectiveRegistry, objective_registry


class ObjectiveManager:

    def __init__(self, stores=None, registry=None, id_generator=None):

        uses_default_stores = stores is None

        self._stores = stores or create_stores(DATA)
        self._registry = registry or (
            objective_registry
            if uses_default_stores
            else ObjectiveRegistry()
        )
        self._id_generator = id_generator or (lambda: str(uuid4()))

        self._load()

    # ---------------------------------

    def _load(self):

        for item in self._stores.objective_db.load():

            objective = Objective(
                item["goal"],
                objective_id=item.get("objective_id"),
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

        for objective in self._registry.records():

            item = {

                "goal": objective.goal,

                "status": objective.status,

                "created": objective.created,

                "started": objective.started,

                "completed": objective.completed,

            }

            if objective.objective_id is not None:
                item["objective_id"] = objective.objective_id

            data.append(item)

        self._stores.objective_db.save(data)

    # ---------------------------------
    # Public save API
    # ---------------------------------

    def save(self):

        self._save()

    # ---------------------------------

    def create(self, goal):

        objective = Objective(goal)

        self._assign_identity(objective)

        self._registry.register(objective)

        self._save()

        return objective

    # ---------------------------------

    def register(self, objective):

        self._assign_identity(objective)

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

    def get_by_id(self, objective_id):

        return self._registry.get_by_id(objective_id)

    # ---------------------------------

    def objectives(self):

        return self._registry.all()

    # ---------------------------------

    def objective_records(self):

        return self._registry.records()

    # ---------------------------------

    def _assign_identity(self, objective):

        if objective.objective_id is None:
            objective._assign_identity(self._id_generator())

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
