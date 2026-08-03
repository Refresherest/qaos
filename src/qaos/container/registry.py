SERVICES = {}


def register(name, service):
    SERVICES[name] = service


def get(name):
    return SERVICES.get(name)


def all():
    return SERVICES