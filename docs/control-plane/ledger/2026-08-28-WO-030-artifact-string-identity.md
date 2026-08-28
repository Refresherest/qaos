# WO-030 — Artifact String Identity Retrieval

## Objective

Make the generic ArtifactManager reliably resolve the string artifact identity
returned to Content OS callers, including after persistence reload.

## Architectural Context

Artifact titles are canonical registry keys. ArtifactRegistry currently checks
`hasattr(key, "title")`; Python strings also expose a `.title` method, so a
string title is converted into a method object and lookup fails. Entity-object
lookups pass, masking the consumer-facing defect.

## Scope

- Correct key normalization in ArtifactRegistry only.
- Add immediate and post-reload string-identity regression coverage.
- Record the finding and update current-state evidence.

## Explicit Non-Goals

- Do not change artifact schema, identity, or persistence format.
- Do not change Memory, Objective, Plan, or other registries.
- Do not change Content OS workflow behavior or add a new slice.
- Do not modify active data, providers, models, or credentials.

## Acceptance Criteria

1. `ArtifactManager.get("title")` returns the registered artifact.
2. A new isolated ArtifactManager over the same stores reloads and resolves the
   persisted artifact by the same string identity.
3. Existing entity-object compatibility lookup continues to work.
4. Focused/full tests and standard verification pass; active data is unchanged.

## Stop Condition

Stop after Artifact string-identity retrieval is reviewed and published. Do not
continue into other registry repairs.
