"""
QAOS Executive Pipeline
"""

from qaos.classifier import classifier_manager
from qaos.council import council_manager
from qaos.planner import planner_manager
from qaos.execution import execution_manager
from qaos.reflection import reflection_manager
from qaos.learning import learning_manager
from qaos.persistence import persistence_manager


class ExecutivePipeline:
    """
    Executes the standard QAOS objective pipeline.
    """

    def execute(
        self,
        objective,
        result,
    ):
        #
        # Classification
        #

        result.classification = (
            classifier_manager.classify(
                objective
            )
        )

        #
        # Council delegation
        #

        result.assignment = (
            council_manager.delegate(
                objective
            )
        )

        #
        # Planning
        #

        result.plan = (
            planner_manager.plan(
                objective
            )
        )

        #
        # Execution
        #

        report = (
            execution_manager.execute(
                objective
            )
        )

        result.execution_report = report

        #
        # Reflection
        #

        reflection = (
            reflection_manager.reflect(
                objective,
                report,
            )
        )

        result.reflection = reflection

        #
        # Learning
        #

        learning_manager.learn(
            reflection
        )

        #
        # Persist
        #

        persistence_manager.save()

        return result


executive_pipeline = ExecutivePipeline()