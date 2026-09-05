"""
QAOS Artifact Manager
"""

from uuid import uuid4

from qaos.storage import create_stores, DATA

from .artifact import Artifact
from .registry import ArtifactRegistry, artifact_registry


class ArtifactManager:

    def __init__(self, stores=None, registry=None, id_generator=None):

        uses_default_stores = stores is None

        self._stores = stores or create_stores(DATA)
        self._registry = registry or (
            artifact_registry
            if uses_default_stores
            else ArtifactRegistry()
        )
        self._id_generator = id_generator or (lambda: str(uuid4()))

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
                artifact_id=item.get("artifact_id"),
                provenance=item.get("provenance"),
                content_sha256=item.get("content_sha256"),

            )

            self._registry.register(artifact)

    # ---------------------------------

    def _save(self):

        data = []

        for artifact in self._registry.records():

            item = {

                "title": artifact.title,
                "artifact_type": artifact.artifact_type,
                "creator": artifact.creator,
                "objective": artifact.objective,
                "content": artifact.content,

            }

            if artifact.artifact_id is not None:
                item["artifact_id"] = artifact.artifact_id
                item["content_sha256"] = artifact.content_sha256
                item["provenance"] = dict(artifact.provenance)

            data.append(item)

        self._stores.artifact_db.save(data)

    # ---------------------------------

    def create(

        self,
        title,
        artifact_type,
        creator,
        objective,
        content,
        provenance=None,

    ):

        artifact = Artifact(

            title=title,
            artifact_type=artifact_type,
            creator=creator,
            objective=objective,
            content=content,
            provenance=provenance,

        )

        self._assign_identity(artifact)

        self._registry.register(artifact)

        self._save()

        return artifact

    # ---------------------------------

    def get(self, title):

        return self._registry.get(title)

    def get_by_id(self, artifact_id):

        return self._registry.get_by_id(artifact_id)

    def artifacts(self):

        return self._registry.all()

    def artifact_records(self):

        return self._registry.records()

    def reload(self):

        self._registry.clear()

        self._load()

    def _assign_identity(self, artifact):

        if artifact.artifact_id is None:
            artifact._assign_identity(self._id_generator())


artifact_manager = ArtifactManager()
