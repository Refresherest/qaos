"""
QAOS Agent Registry
"""

AGENTS = {}


def register(agent):
    AGENTS[agent.name] = agent


def unregister(name):
    AGENTS.pop(name, None)


def get(name):
    return AGENTS.get(name)


def all_agents():
    return AGENTS