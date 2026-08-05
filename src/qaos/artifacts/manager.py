"""
QAOS Artifact Manager
"""

from .artifact import Artifact
from .registry import (
    register,
    get,
    all,
)


class ArtifactManager:

    def create(
        self,
        title,
        artifact_type,
        creator,
        objective,
        content,
    ):

        artifact = Artifact(
            title,
            artifact_type,
            creator,
            objective,
            content,
        )

        register(artifact)

        return artifact

    def get(self, title):

        return get(title)

    def artifacts(self):

        return all()


artifact_manager = ArtifactManager()