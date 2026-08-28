"""
QAOS Artifact Registry
"""

class ArtifactRegistry:
    """Registry state owned by one artifact-manager lifecycle."""

    def __init__(self):
        self._registry = {}

    def register(self, artifact):
        self._registry[artifact.title] = artifact

    def get(self, title):
        if not isinstance(title, str) and hasattr(title, "title"):
            title = title.title

        return self._registry.get(title)

    def all(self):
        return self._registry


artifact_registry = ArtifactRegistry()


def register(artifact):
    artifact_registry.register(artifact)


def get(title):
    return artifact_registry.get(title)


def all():
    return artifact_registry.all()
