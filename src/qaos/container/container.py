from .registry import register, get, all


class ServiceContainer:

    def register(self, name, service):
        register(name, service)

    def get(self, name):
        return get(name)

    def services(self):
        return all()


container = ServiceContainer()