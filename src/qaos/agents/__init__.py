"""
QAOS Agents
"""

from .agent import Agent

from .manager import (
    AgentManager,
    agent_manager,
)

from .registry import (
    register,
    unregister,
    get,
    all,
)

#
# Register the default agent
#

register(
    Agent("default")
)

__all__ = [

    "Agent",

    "AgentManager",
    "agent_manager",

    "register",
    "unregister",
    "get",
    "all",
]