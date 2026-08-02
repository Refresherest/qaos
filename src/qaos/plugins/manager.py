"""
QAOS Plugin Manager
"""

from qaos.plugins.registry import register


class PluginManager:

    def __init__(self):
        self.loaded = []

    def load_builtin(self):
        """
        Load built-in QAOS plugins.
        """

        register(
            "core",
            {
                "name": "Core Plugin",
                "version": "0.1.0",
            },
        )

        self.loaded.append("core")

    def plugins(self):
        return self.loaded