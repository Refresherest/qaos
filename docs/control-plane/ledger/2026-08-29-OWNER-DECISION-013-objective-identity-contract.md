# OWNER-DECISION-013 — Objective Identity Contract

## Decision

The owner selected **Option A — Manager-Injected IDs with Dual Indexes** from
DECISION-REQUEST-013.

## Governing Contract

- Objective may begin with an unassigned `objective_id`.
- ObjectiveManager owns an injected zero-argument ID generator. Its default
  produces a provider-neutral opaque string; UUID4 formatting is an
  implementation detail. Tests may inject deterministic generators.
- Creating or newly registering an unidentified Objective assigns exactly one
  ID. A different ID must not later replace it.
- Legacy loading is a distinct path and never invents a missing ID.
- ObjectiveRegistry maintains canonical `objective_id -> Objective` lookup and
  a `goal -> latest registered Objective` compatibility projection.
- Unidentified legacy Objectives remain retained and accessible through goal
  compatibility lookup.
- Object lookup prefers identity and uses goal only for an unidentified
  Objective. String goal lookup retains existing latest-by-goal behavior.
- Explicit ID lookup is separate; arbitrary strings are never guessed to be
  IDs rather than goals.
- Goal-keyed `all()` may remain temporarily as a compatibility projection, but
  persistence must use complete-record iteration so equal goals are preserved.
- New identified records write `objective_id`. Legacy missing-ID records load
  as unidentified and retain their original serialized shape; unrelated saves
  must not synthesize IDs for them.
- Duplicate non-null IDs fail closed. The exact error type is a bounded
  implementation decision.
- Identity is never derived from goal text, timestamps, content, or position.

## Scope Boundary

This decision authorizes a separate bounded implementation work order for the
Objective identity foundation only. It does not authorize Plan or QueueItem
propagation, active-data migration, recovery behavior, credentials, provider
settings, or unrelated QAOS changes.
