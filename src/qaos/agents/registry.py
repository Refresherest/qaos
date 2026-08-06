"""
QAOS Agent Registry
"""

AGENTS = {}


def register(agent):
    """
    Register an Agent instance.
    """
    AGENTS[agent.name] = agent


def unregister(name):
    """
    Remove an Agent.
    """
    AGENTS.pop(name, None)


def get(name):
    """
    Retrieve an Agent.
    """
    return AGENTS.get(name)


def all():
    """
    Return all registered agents.
    """
    return AGENTS