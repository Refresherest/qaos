"""
QAOS Capabilities
"""

from .capability import Capability

from .manager import (
    CapabilityManager,
    capability_manager,
)

from .system import (
    SystemCapability,
    system_capability,
)
from .registry import register

#
# Register the default system capability
#

register(system_capability)

__all__ = [
    "Capability",
    "CapabilityManager",
    "capability_manager",
    "SystemCapability",
    "system_capability",
]
