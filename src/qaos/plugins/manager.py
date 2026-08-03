"""
QAOS Plugin Manager
"""

from qaos.plugins.registry import (
    register,
    unregister,
    get,
    all_plugins,
)


class PluginManager:

    def register(self, plugin):

        register(plugin.name, plugin)

    def unregister(self, name):

        unregister(name)

    def get(self, name):

        return get(name)

    def plugins(self):

        return all_plugins()

    def initialize(self):

        for plugin in all_plugins().values():
            plugin.initialize()

    def shutdown(self):

        for plugin in all_plugins().values():
            plugin.shutdown()


plugin_manager = PluginManager()