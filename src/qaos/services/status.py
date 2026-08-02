from qaos.config import configuration
from qaos.agents.registry import AGENTS
from qaos.council.registry import EXECUTIVE_COUNCIL
from qaos.plugins.registry import PLUGINS


class StatusService:

    def get_status(self):
        return {
            "kernel": "Running",
            "runtime": "Running",
            "configuration": "Loaded",
            "environment": configuration.environment,
            "version": configuration.version,
            "agents": len(AGENTS),
            "council": len(EXECUTIVE_COUNCIL),
            "plugins": len(PLUGINS),
            "status": "HEALTHY",
        }


status_service = StatusService()