class StatusService:

    def __init__(self, configuration, agent_manager, council_manager, plugin_manager):
        self.configuration = configuration
        self.agent_manager = agent_manager
        self.council_manager = council_manager
        self.plugin_manager = plugin_manager

    def get_status(self):
        return {
            "kernel": "Running",
            "runtime": "Running",
            "configuration": "Loaded",
            "environment": self.configuration.get("environment"),
            "version": self.configuration.get("version"),
            "agents": len(self.agent_manager.agents()),
            "council": len(self.council_manager.members()),
            "plugins": len(self.plugin_manager.plugins()),
            "status": "HEALTHY",
        }
