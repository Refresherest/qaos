# FINDING-005 — Artifact String-Key Lookup

## Status

`RESOLVED — WO-030`

## Evidence

ArtifactRegistry used `hasattr(title, "title")` to distinguish Artifact objects
from title strings. Because `str.title` exists, string lookup used the bound
method as the dictionary key and returned no artifact.

## Impact

Content OS returns artifact identity as a string-facing title, but a caller
could not resolve that identity through ArtifactManager, including after reload.

## Resolution

WO-030 treats strings as canonical title keys and only extracts `.title` from
non-string entity objects. Immediate, entity-object, and post-reload lookups are
covered by focused tests.

## Remaining Boundary

Similar behavior in other registries remains outside WO-030 and requires
separate work orders if prioritized.
