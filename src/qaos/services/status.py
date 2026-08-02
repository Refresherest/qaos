from qaos.config import configuration
from qaos.agents.registry import AGENTS
from qaos.council.registry import EXECUTIVE_COUNCIL


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
            "status": "HEALTHY",
        }


status_service = StatusService()