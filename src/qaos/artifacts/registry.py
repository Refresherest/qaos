"""
QAOS Artifact Registry
"""

class ArtifactRegistry:
    """Registry state owned by one artifact-manager lifecycle."""

    def __init__(self):
        self._by_id = {}
        self._by_title = {}
        self._records = []

    def register(self, artifact):
        artifact_id = getattr(artifact, "artifact_id", None)
        if artifact_id is not None:
            existing = self._by_id.get(artifact_id)
            if existing is not None and existing is not artifact:
                raise ValueError(f"duplicate artifact_id: {artifact_id}")
            self._by_id[artifact_id] = artifact

        if artifact not in self._records:
            self._records.append(artifact)

        self._by_title[artifact.title] = artifact

    def get(self, title):
        if not isinstance(title, str) and hasattr(title, "title"):
            artifact_id = getattr(title, "artifact_id", None)
            if artifact_id is not None:
                return self._by_id.get(artifact_id)
            title = title.title

        return self._by_title.get(title)

    def get_by_id(self, artifact_id):
        return self._by_id.get(artifact_id)

    def records(self):
        return tuple(self._records)

    def clear(self):
        self._by_id.clear()
        self._by_title.clear()
        self._records.clear()

    def all(self):
        return self._by_title


artifact_registry = ArtifactRegistry()


def register(artifact):
    artifact_registry.register(artifact)


def get(title):
    return artifact_registry.get(title)


def all():
    return artifact_registry.all()
