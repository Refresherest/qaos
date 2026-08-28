from qaos.config import Configuration
from qaos.services.container import ServiceContainer


class Runtime:
    def __init__(self, configuration, services=None):
        self.config = configuration
        self.services = services if services is not None else ServiceContainer()

    def register(self, name, service):
        self.services.register(name, service)

    def get(self, name):
        return self.services.get(name)


def create_runtime(configuration, *, logger=None, event_bus=None, executive=None):
    """Compose a Runtime from explicit dependencies without global state."""
    if not isinstance(configuration, Configuration):
        raise TypeError("configuration must be a Configuration instance")

    runtime = Runtime(configuration)
    if logger is not None:
        runtime.register("logger", logger)
    if event_bus is not None:
        runtime.register("events", event_bus)
    if executive is not None:
        runtime.register("executive", executive)
    return runtime
