"""
QAOS Default Worker
"""

from qaos.agents import agent_manager


class DefaultWorker:
    """
    Default QAOS Worker.

    Workers supervise execution.

    They do not perform work themselves.
    """

    name = "default"

    def __init__(self, agents=None):
        self._agents = agent_manager if agents is None else agents

    # ----------------------------------

    def execute(self, item):

        print(
            f"[Worker:{self.name}] "
            f"Executing '{item.objective}'"
        )

        #
        # Resolve the default agent
        #

        agent = self._agents.get(
            "default"
        )

        if agent is None:

            raise RuntimeError(
                "No default agent registered."
            )

        #
        # Delegate execution
        #

        return agent.execute(item)

    # ----------------------------------

    def __repr__(self):

        return "<DefaultWorker>"


default_worker = DefaultWorker()
