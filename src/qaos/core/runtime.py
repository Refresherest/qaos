from qaos.config import config
from qaos.logging import logger

class Runtime:
    def __init__(self):
        self.config = config
        self.services = {}
        self.register("logger", logger)

    def register(self, name, service):
        self.services[name] = service

    def get(self, name):
        return self.services.get(name)


runtime = Runtime()