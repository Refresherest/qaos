"""
QAOS Artifact
"""

import hashlib
import json
from types import MappingProxyType


MAX_PROVENANCE_ENTRIES = 16
MAX_PROVENANCE_KEY_BYTES = 64
MAX_PROVENANCE_VALUE_BYTES = 1024
MAX_PROVENANCE_BYTES = 8192


class Artifact:

    def __init__(
        self,
        title,
        artifact_type,
        creator,
        objective,
        content,
        artifact_id=None,
        provenance=None,
        content_sha256=None,
    ):

        if not isinstance(content, str):
            raise TypeError("artifact content must be a string")

        self.title = title
        self.artifact_type = artifact_type
        self.creator = creator
        self.objective = objective

        self._artifact_id = None
        if artifact_id is not None:
            self._assign_identity(artifact_id)

        self._content = content
        derived_digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
        if content_sha256 is not None and content_sha256 != derived_digest:
            raise ValueError("content_sha256 does not match artifact content")
        self._content_sha256 = derived_digest
        self._provenance = MappingProxyType(self._validate_provenance(provenance))

    @property
    def artifact_id(self):
        return self._artifact_id

    def _assign_identity(self, artifact_id):
        if not isinstance(artifact_id, str) or not artifact_id:
            raise ValueError("artifact_id must be a non-empty string")

        if self._artifact_id is not None and self._artifact_id != artifact_id:
            raise ValueError("artifact_id is immutable once assigned")

        self._artifact_id = artifact_id

    @property
    def content(self):
        return self._content

    @property
    def content_sha256(self):
        return self._content_sha256

    @property
    def provenance(self):
        return self._provenance

    @staticmethod
    def _validate_provenance(provenance):
        if provenance is None:
            return {}
        if not isinstance(provenance, dict):
            raise TypeError("artifact provenance must be a dictionary")
        if len(provenance) > MAX_PROVENANCE_ENTRIES:
            raise ValueError("artifact provenance has too many entries")

        validated = {}
        for key, value in provenance.items():
            if not isinstance(key, str) or not key:
                raise ValueError("artifact provenance keys must be non-empty strings")
            if not isinstance(value, str) or not value:
                raise ValueError(
                    "artifact provenance values must be non-empty strings"
                )
            if len(key.encode("utf-8")) > MAX_PROVENANCE_KEY_BYTES:
                raise ValueError("artifact provenance key is too long")
            if len(value.encode("utf-8")) > MAX_PROVENANCE_VALUE_BYTES:
                raise ValueError("artifact provenance value is too long")
            validated[key] = value

        encoded = json.dumps(
            validated,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
        if len(encoded) > MAX_PROVENANCE_BYTES:
            raise ValueError("artifact provenance is too large")
        return validated

    def __repr__(self):

        return f"<Artifact {self.title}>"
