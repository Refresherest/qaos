"""
QAOS Executive Council Registry
"""

_COUNCIL = {}


def register(member):
    """
    Register an Executive Council member.
    """
    _COUNCIL[member.name] = member


def get(name):
    """
    Return a council member.
    """
    return _COUNCIL.get(name)


def all():
    """
    Return all registered members.
    """
    return dict(_COUNCIL)