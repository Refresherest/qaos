"""
QAOS Agent Resolver
"""

from .registry import all


class AgentResolver:
    """
    Resolves the most appropriate agent
    for a QueueItem.
    """

    def resolve(self, item):

        agents = all()

        #
        # Temporary implementation.
        #
        # Later this becomes capability,
        # load, role and specialization
        # aware.
        #

        if not agents:

            raise RuntimeError(
                "No agents registered."
            )

        return next(
            iter(agents.values())
        )


agent_resolver = AgentResolver()