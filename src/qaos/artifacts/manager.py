"""
QAOS Artifact Manager
"""

from qaos.storage import create_stores, DATA

from .artifact import Artifact
from .registry import ArtifactRegistry, artifact_registry


class ArtifactManager:

    def __init__(self, stores=None, registry=None):

        uses_default_stores = stores is None

        self._stores = stores or create_stores(DATA)
        self._registry = registry or (
            artifact_registry
            if uses_default_stores
            else ArtifactRegistry()
        )

        self._load()

    # ---------------------------------

    def _load(self):

        for item in self._stores.artifact_db.load():

            artifact = Artifact(

                title=item["title"],
                artifact_type=item["artifact_type"],
                creator=item["creator"],
                objective=item["objective"],
                content=item["content"],

            )

            self._registry.register(artifact)

    # ---------------------------------

    def _save(self):

        data = []

        for artifact in self._registry.all().values():

            data.append({

                "title": artifact.title,
                "artifact_type": artifact.artifact_type,
                "creator": artifact.creator,
                "objective": artifact.objective,
                "content": artifact.content,

            })

        self._stores.artifact_db.save(data)

    # ---------------------------------

    def create(

        self,
        title,
        artifact_type,
        creator,
        objective,
        content,

    ):

        artifact = Artifact(

            title=title,
            artifact_type=artifact_type,
            creator=creator,
            objective=objective,
            content=content,

        )

        self._registry.register(artifact)

        self._save()

        return artifact

    # ---------------------------------

    def get(self, title):

        return self._registry.get(title)

    def artifacts(self):

        return self._registry.all()

    def reload(self):

        self._registry.all().clear()

        self._load()


artifact_manager = ArtifactManager()
