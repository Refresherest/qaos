from qaos.config import config
from qaos.logging import logger
from qaos.services import ServiceContainer
from qaos.events import event_bus


class Runtime:
    def __init__(self):
        self.config = config
        self.services = ServiceContainer()

        self.register("logger", logger)
        self.register("events", event_bus)

    def register(self, name, service):
        self.services.register(name, service)

    def get(self, name):
        return self.services.get(name)


runtime = Runtime()