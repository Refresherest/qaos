"""
QAOS Artifacts
"""

from .artifact import Artifact

from .manager import (
    ArtifactManager,
    artifact_manager,
)

from .registry import (
    register,
    get,
    all,
)

__all__ = [
    "Artifact",
    "ArtifactManager",
    "artifact_manager",
    "register",
    "get",
    "all",
]