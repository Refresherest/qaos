"""
QAOS Agent Registry
"""

class AgentRegistry:
    """Registry state owned by one agent-manager lifecycle."""

    def __init__(self):
        self._agents = {}

    def register(self, agent):
        self._agents[agent.name] = agent

    def unregister(self, name):
        self._agents.pop(name, None)

    def get(self, name):
        return self._agents.get(name)

    def all(self):
        return self._agents


agent_registry = AgentRegistry()


def register(agent):
    """
    Register an Agent instance.
    """
    agent_registry.register(agent)


def unregister(name):
    """
    Remove an Agent.
    """
    agent_registry.unregister(name)


def get(name):
    """
    Retrieve an Agent.
    """
    return agent_registry.get(name)


def all():
    """
    Return all registered agents.
    """
    return agent_registry.all()
