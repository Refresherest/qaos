"""
QAOS Capability Framework
"""

from .base import Capability
from .manager import (
    CapabilityManager,
    capability_manager,
)

from .filesystem import FilesystemCapability

filesystem = FilesystemCapability()

capability_manager.register(filesystem)

__all__ = [
    "Capability",
    "CapabilityManager",
    "capability_manager",
    "filesystem",
]