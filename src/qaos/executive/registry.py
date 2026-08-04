"""
QAOS Executive Registry
"""

_EXECUTIVES = {}


def register(profile):

    _EXECUTIVES[profile.title] = profile


def get(title):

    return _EXECUTIVES.get(title)


def all():

    return _EXECUTIVES