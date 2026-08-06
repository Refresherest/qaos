"""
QAOS Reflection
"""


class Reflection:

    def __init__(
        self,
        objective,
        summary="",
        successes=None,
        failures=None,
    ):

        self.objective = objective

        self.summary = summary

        self.successes = successes or []

        self.failures = failures or []

    # ----------------------------------

    def add_success(self, text):

        self.successes.append(text)

    # ----------------------------------

    def add_failure(self, text):

        self.failures.append(text)

    # ----------------------------------

    def __repr__(self):

        if hasattr(self.objective, "goal"):
            objective = self.objective.goal
        else:
            objective = self.objective

        return f"<Reflection {objective}>"