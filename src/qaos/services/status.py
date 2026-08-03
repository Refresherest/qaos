from qaos.config import configuration
from qaos.agents import agent_manager
from qaos.council import council_manager
from qaos.plugins import plugin_manager


class StatusService:

    def get_status(self):
        return {
            "kernel": "Running",
            "runtime": "Running",
            "configuration": "Loaded",
            "environment": configuration.environment,
            "version": configuration.version,
            "agents": len(agent_manager.agents()),
            "council": len(council_manager.members()),
            "plugins": len(plugin_manager.plugins()),
            "status": "HEALTHY",
        }


status_service = StatusService()