"""
QAOS Plugin Registry
"""


PLUGINS = {}


def register(name, plugin):
    """
    Register a plugin.
    """
    PLUGINS[name] = plugin


def unregister(name):
    """
    Remove a plugin.
    """
    PLUGINS.pop(name, None)


def get(name):
    """
    Retrieve a plugin.
    """
    return PLUGINS.get(name)


def all_plugins():
    """
    Return every registered plugin.
    """
    return PLUGINS