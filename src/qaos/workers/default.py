"""
QAOS Default Worker
"""

from datetime import datetime

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

        item.status = "running"
        item.started = datetime.now()

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

        try:
            result = agent.execute(item)
        except Exception:
            if item.status == "running":
                item.status = "failed"
                item.completed = datetime.now()

            action = item.action
            if (
                getattr(action, "status", None) == "running"
                and callable(getattr(action, "fail", None))
            ):
                action.fail()

            raise

        item.status = "completed"
        item.completed = datetime.now()

        if item.result is None:
            item.result = f"Completed: {item.objective}"

        return result

    # ----------------------------------

    def __repr__(self):

        return "<DefaultWorker>"


default_worker = DefaultWorker()
