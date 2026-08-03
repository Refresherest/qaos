"""
QAOS Task Registry
"""

TASKS = {}


def register(name, task):
    TASKS[name] = task


def unregister(name):
    TASKS.pop(name, None)


def get(name):
    return TASKS.get(name)


def all_tasks():
    return TASKS