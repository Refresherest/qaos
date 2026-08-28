# WO-031 — Memory String Identity Lifecycle

## Objective

Make MemoryManager reliably resolve and unregister canonical string memory
titles, including after persistence reload.

## Architectural Context

Memory titles are registry keys. MemoryRegistry checks `hasattr(key, "title")`
for both lookup and removal; Python strings expose `.title`, so canonical string
keys become bound methods and both operations fail.

## Scope

- Correct `get` and `unregister` key normalization in MemoryRegistry only.
- Add immediate, post-reload, and persisted-unregister regression coverage.
- Record the finding and update current-state evidence.

## Explicit Non-Goals

- Do not change memory schema, identity, or persistence format.
- Do not change Artifact, Objective, Plan, or other registries.
- Do not modify Content OS, providers, models, credentials, or active data.

## Acceptance Criteria

1. `MemoryManager.get("title")` returns the registered memory.
2. A new manager over the same stores reloads and resolves the same title.
3. `unregister("title")` removes the in-memory and persisted record.
4. Entity-object compatibility lookup/removal continues to work.
5. Focused/full tests and standard verification pass; active data is unchanged.

## Stop Condition

Stop after Memory string-identity lifecycle behavior is reviewed and published.
