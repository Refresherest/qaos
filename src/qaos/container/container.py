"""
QAOS Service Container
"""

from qaos.container.registry import (
    register,
    unregister,
    get,
    all_services,
)


class ServiceContainer:

    def register(self, name, service):
        register(name, service)

    def unregister(self, name):
        unregister(name)

    def get(self, name):
        return get(name)

    def services(self):
        return all_services()

    def clear(self):
        all_services().clear()


container = ServiceContainer()