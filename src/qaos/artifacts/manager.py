"""
QAOS Artifact Manager
"""

from qaos.storage import create_stores, DATA

from .artifact import Artifact
from .registry import (
    register,
    get,
    all,
)


class ArtifactManager:

    def __init__(self, stores=None):

        self._stores = stores or create_stores(DATA)

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

            register(artifact)

    # ---------------------------------

    def _save(self):

        data = []

        for artifact in all().values():

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

        register(artifact)

        self._save()

        return artifact

    # ---------------------------------

    def get(self, title):

        return get(title)

    def artifacts(self):

        return all()

    def reload(self):

        all().clear()

        self._load()


artifact_manager = ArtifactManager()