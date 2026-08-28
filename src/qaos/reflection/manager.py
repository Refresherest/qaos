"""
QAOS Reflection Manager
"""

from qaos.storage import create_stores, DATA

from .reflection import Reflection
from .registry import ReflectionRegistry, reflection_registry


class ReflectionManager:

    def __init__(self, stores=None, registry=None):

        uses_default_stores = stores is None
        self._stores = stores or create_stores(DATA)
        self._registry = registry or (
            reflection_registry
            if uses_default_stores
            else ReflectionRegistry()
        )

        self._load()

    # -------------------------------------------------

    def _load(self):

        for item in self._stores.reflection_db.load():

            reflection = Reflection(

                objective=item["objective"],

                summary=item.get(
                    "summary",
                    "",
                ),

                successes=item.get(
                    "successes",
                    [],
                ),

                failures=item.get(
                    "failures",
                    [],
                ),

            )

            self._registry.register(reflection)

    # -------------------------------------------------

    def _save(self):

        data = []

        for reflection in self._registry.all().values():

            objective = reflection.objective

            if hasattr(objective, "goal"):

                objective = objective.goal

            data.append({

                "objective": objective,

                "summary": reflection.summary,

                "successes": reflection.successes,

                "failures": reflection.failures,

            })

        self._stores.reflection_db.save(data)

    # -------------------------------------------------

    def create(

        self,
        objective,
        summary="",
        successes=None,
        failures=None,

    ):

        reflection = Reflection(

            objective=objective,

            summary=summary,

            successes=successes or [],

            failures=failures or [],

        )

        self._registry.register(reflection)

        self._save()

        return reflection

    # -------------------------------------------------

    def reflect(
        self,
        objective,
        report,
    ):
        """
        Convert an ExecutionReport into
        a persistent Reflection.
        """

        summary = ""

        successes = []

        failures = []

        if getattr(report, "success", False):

            summary = "Objective completed successfully."

            successes.append(summary)

        else:

            summary = "Objective execution failed."

            failures.append(summary)

        reflection = Reflection(

            objective=objective,

            summary=summary,

            successes=successes,

            failures=failures,

        )

        self._registry.register(reflection)

        self._save()

        return reflection

    # -------------------------------------------------

    def register(self, reflection):

        self._registry.register(reflection)

        self._save()

    # -------------------------------------------------

    def unregister(self, objective):

        self._registry.unregister(objective)

        self._save()

    # -------------------------------------------------

    def get(self, objective):

        return self._registry.get(objective)

    # -------------------------------------------------

    def reflections(self):

        return self._registry.all()

    # -------------------------------------------------

    def save(self):

        self._save()


reflection_manager = ReflectionManager()
