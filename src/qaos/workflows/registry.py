"""
QAOS Workflow Registry
"""

WORKFLOWS = {}


def register(workflow):
    WORKFLOWS[workflow.name] = workflow


def unregister(name):
    WORKFLOWS.pop(name, None)


def get(name):
    return WORKFLOWS.get(name)


def all_workflows():
    return WORKFLOWS