"""
QAOS Objective Registry
"""

_OBJECTIVES = []


def register(objective):
    _OBJECTIVES.append(objective)


def all():
    return list(_OBJECTIVES)


def clear():
    _OBJECTIVES.clear()