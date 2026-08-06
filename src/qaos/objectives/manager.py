"""
QAOS Objective Manager
"""

from qaos.storage import objective_db

from .objective import Objective
from .registry import (
    register,
    unregister,
    get,
    all,
)


class ObjectiveManager:

    def __init__(self):

        self._load()

    # ---------------------------------

    def _load(self):

        for item in objective_db.load():

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

            register(objective)

    # ---------------------------------

    def _save(self):

        data = []

        for objective in all().values():

            data.append({

                "goal": objective.goal,

                "status": objective.status,

                "created": objective.created,

                "started": objective.started,

                "completed": objective.completed,

            })

        objective_db.save(data)

    # ---------------------------------
    # Public save API
    # ---------------------------------

    def save(self):

        self._save()

    # ---------------------------------

    def create(self, goal):

        objective = Objective(goal)

        register(objective)

        self._save()

        return objective

    # ---------------------------------

    def register(self, objective):

        register(objective)

        self._save()

    # ---------------------------------

    def unregister(self, goal):

        unregister(goal)

        self._save()

    # ---------------------------------

    def get(self, goal):

        return get(goal)

    # ---------------------------------

    def objectives(self):

        return all()


objective_manager = ObjectiveManager()