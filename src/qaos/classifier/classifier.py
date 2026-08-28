"""
QAOS Intent Classifier
"""


class IntentClassifier:

    def __init__(self, fallback=None):

        self._rules = {}
        self._fallback = fallback

    # -------------------------------------------------

    def register(
        self,
        keyword,
        skill,
    ):

        self._rules[
            keyword.lower()
        ] = skill

    # -------------------------------------------------

    def classify(
        self,
        objective,
    ):
        """
        Classify either a plain string or
        a QAOS Objective.

        Supported:

            classify("Build website")

            classify(objective)
        """

        #
        # Extract text
        #

        if isinstance(
            objective,
            str,
        ):

            text = objective

        elif hasattr(
            objective,
            "goal",
        ):

            text = objective.goal

        elif hasattr(
            objective,
            "objective",
        ):

            text = objective.objective

        elif hasattr(
            objective,
            "title",
        ):

            text = objective.title

        else:

            text = str(
                objective
            )

        text = text.lower()

        #
        # Match rules
        #

        for (
            keyword,
            skill,
        ) in self._rules.items():

            if keyword in text:

                return skill

        return self._fallback

    # -------------------------------------------------

    def __repr__(self):

        return (
            f"<IntentClassifier "
            f"{len(self._rules)} rules>"
        )
