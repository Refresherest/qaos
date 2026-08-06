"""
QAOS Learning Engine
"""

from qaos.memory import memory_manager
from qaos.knowledge import knowledge_manager


class LearningEngine:

    def learn(self, reflection):

        if hasattr(reflection.objective, "goal"):
            goal = reflection.objective.goal
        else:
            goal = reflection.objective

        print(
            f"[Learning] Processing: {goal}"
        )

        memory_count = 0
        knowledge_count = 0

        # ---------------------------------
        # Store summary
        # ---------------------------------

        if reflection.summary:

            memory_manager.create(
                title=goal,
                content=reflection.summary,
                category="reflection",
            )

            memory_count += 1

        # ---------------------------------
        # Store successes
        # ---------------------------------

        for success in reflection.successes:

            memory_manager.create(
                title=goal,
                content=success,
                category="success",
            )

            knowledge_manager.create(
                title=goal,
                category="Experience",
                content=success,
                source="Learning Engine",
            )

            memory_count += 1
            knowledge_count += 1

        # ---------------------------------
        # Store failures
        # ---------------------------------

        for failure in reflection.failures:

            memory_manager.create(
                title=goal,
                content=failure,
                category="failure",
            )

            memory_count += 1

        return {

            "memory": memory_count,

            "knowledge": knowledge_count,

        }


learning_engine = LearningEngine()