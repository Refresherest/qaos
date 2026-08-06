"""
QAOS Capability Registry
"""

_CAPABILITIES = {}


def register(capability):
    """
    Register a capability.
    """

    _CAPABILITIES[
        capability.name
    ] = capability


# ----------------------------------


def unregister(name):
    """
    Remove a capability.
    """

    _CAPABILITIES.pop(
        name,
        None,
    )


# ----------------------------------


def get(name):
    """
    Return a capability.
    """

    return _CAPABILITIES.get(name)


# ----------------------------------


def all():
    """
    Return all capabilities.
    """

    return dict(
        _CAPABILITIES
    )


# ----------------------------------


def clear():
    """
    Remove every registered capability.
    """

    _CAPABILITIES.clear()