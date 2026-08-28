"""
QAOS Executive Pipeline
"""

from qaos.classifier import classifier_manager
from qaos.council import council_manager
from qaos.planner import planner_manager
from qaos.execution import execution_manager
from qaos.reflection import reflection_manager
from qaos.learning import learning_manager


class ExecutivePipeline:
    """
    Executes the standard QAOS objective pipeline.
    """

    def __init__(
        self,
        *,
        classifier=None,
        council=None,
        planner=None,
        execution=None,
        reflection=None,
        learning=None,
    ):
        self._classifier = (
            classifier_manager if classifier is None else classifier
        )
        self._council = council_manager if council is None else council
        self._planner = planner_manager if planner is None else planner
        self._execution = execution_manager if execution is None else execution
        self._reflection = (
            reflection_manager if reflection is None else reflection
        )
        self._learning = learning_manager if learning is None else learning

    def execute(
        self,
        objective,
        result,
    ):
        #
        # Classification
        #

        result.classification = (
            self._classifier.classify(
                objective
            )
        )

        #
        # Council delegation
        #

        result.assignment = (
            self._council.delegate(
                objective
            )
        )

        #
        # Planning
        #

        result.plan = (
            self._planner.plan(
                objective
            )
        )

        #
        # Execution
        #

        report = (
            self._execution.execute(
                objective
            )
        )

        result.execution_report = report

        #
        # Reflection
        #

        reflection = (
            self._reflection.reflect(
                objective,
                report,
            )
        )

        result.reflection = reflection

        #
        # Learning
        #

        self._learning.learn(
            reflection
        )

        return result


executive_pipeline = ExecutivePipeline()
