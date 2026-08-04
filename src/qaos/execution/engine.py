"""
QAOS Execution Engine
"""


class ExecutionEngine:

    def execute(self, objective):

        print("=" * 50)
        print("QAOS Execution Engine")
        print("=" * 50)
        print()

        print(f"Objective : {objective.goal}")

        objective.start()

        if objective.plan:

            objective.plan.execute()

        objective.complete()

        print()
        print("Status:", objective.status)