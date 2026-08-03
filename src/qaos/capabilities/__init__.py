"""
QAOS Capability Framework
"""

from .base import Capability
from .manager import CapabilityManager, capability_manager

from .filesystem import FilesystemCapability
from .git import GitCapability

# Register built-in capabilities.
capability_manager.register(
    FilesystemCapability()
)

capability_manager.register(
    GitCapability()
)

__all__ = [
    "Capability",
    "CapabilityManager",
    "capability_manager",
]