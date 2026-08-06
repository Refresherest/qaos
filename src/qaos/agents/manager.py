"""
QAOS Agent Manager
"""

from qaos.agents.registry import (
    register,
    unregister,
    get,
    all,
)


class AgentManager:

    def register(self, agent):
        register(agent)

    def unregister(self, name):
        unregister(name)

    def get(self, name):
        return get(name)

    def agents(self):
        return all()

    def initialize(self):
        for agent in all().values():
            if hasattr(agent, "initialize"):
                agent.initialize()

    def shutdown(self):
        for agent in all().values():
            if hasattr(agent, "shutdown"):
                agent.shutdown()

    def execute(self, name, item):

        agent = get(name)

        if agent is None:
            raise ValueError(
                f"Unknown agent: {name}"
            )

        return agent.execute(item)


agent_manager = AgentManager()