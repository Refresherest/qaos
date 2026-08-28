"""
QAOS Agent Manager
"""

from qaos.agents.registry import agent_registry


class AgentManager:

    def __init__(self, registry=None):
        self._registry = agent_registry if registry is None else registry

    def register(self, agent):
        self._registry.register(agent)

    def unregister(self, name):
        self._registry.unregister(name)

    def get(self, name):
        return self._registry.get(name)

    def agents(self):
        return self._registry.all()

    def initialize(self):
        for agent in self._registry.all().values():
            if hasattr(agent, "initialize"):
                agent.initialize()

    def shutdown(self):
        for agent in self._registry.all().values():
            if hasattr(agent, "shutdown"):
                agent.shutdown()

    def execute(self, name, item):

        agent = self._registry.get(name)

        if agent is None:
            raise ValueError(
                f"Unknown agent: {name}"
            )

        return agent.execute(item)


agent_manager = AgentManager()
