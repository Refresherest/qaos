"""
QAOS Bootstrap Package
"""

from .boot import BootManager, boot_manager
from .registry import register

from .steps import (
    initialize_logger,
    initialize_plugins,
)

register(initialize_logger)
register(initialize_plugins)

__all__ = [
    "BootManager",
    "boot_manager",
    "register",
]