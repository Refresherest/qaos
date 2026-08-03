WORKFLOWS = {}


def register(name, workflow):
    WORKFLOWS[name] = workflow


def get(name):
    return WORKFLOWS.get(name)


def all():
    return WORKFLOWS