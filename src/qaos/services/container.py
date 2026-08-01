class ServiceContainer:
    def __init__(self):
        self._services = {}

    def register(self, name, service):
        self._services[name] = service

    def get(self, name):
        return self._services.get(name)

    def exists(self, name):
        return name in self._services

    def all(self):
        return list(self._services.keys())