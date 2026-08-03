"""
QAOS Service Registry
"""

SERVICES = {}


def register(name, service):
    SERVICES[name] = service


def unregister(name):
    SERVICES.pop(name, None)


def get(name):
    return SERVICES.get(name)


def all_services():
    return SERVICES