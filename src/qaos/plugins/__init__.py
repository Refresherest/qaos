"""
QAOS Plugin System
"""

from .manager import PluginManager

plugin_manager = PluginManager()

__all__ = [
    "PluginManager",
    "plugin_manager",
]