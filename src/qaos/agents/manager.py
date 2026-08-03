"""
QAOS Agent Manager
"""

from qaos.agents.registry import (
    register,
    unregister,
    get,
    all_agents,
)


class AgentManager:

    def register(self, agent):
        register(agent)

    def unregister(self, name):
        unregister(name)

    def get(self, name):
        return get(name)

    def agents(self):
        return all_agents()

    def initialize(self):
        for agent in all_agents().values():
            agent.initialize()

    def shutdown(self):
        for agent in all_agents().values():
            agent.shutdown()

    def execute(self, name):
        agent = get(name)

        if agent:
            return agent.run()


agent_manager = AgentManager()