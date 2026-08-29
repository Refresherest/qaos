# PROPOSAL-006 — Objective Identity Contract

## Evidence Summary

- Objective currently has no identity field.
- ObjectiveManager constructs new and reloaded Objectives.
- ObjectiveRegistry uses one goal-keyed dictionary.
- Re-registering equal goal text replaces the earlier Objective.
- `get(goal)`, `get(objective)`, and goal-keyed `all()` are existing
  compatibility behavior used by tests and managers.
- ObjectiveManager saves `all().values()`, so a single goal index cannot retain
  repeated equal-goal invocations.

## Recommended Contract

### ID Generation

- Objective supports an initially unassigned `objective_id`.
- ObjectiveManager owns an injected zero-argument ID generator.
- The default generator returns a provider-neutral opaque string, using UUID4
  formatting as an implementation detail rather than domain meaning.
- Tests inject deterministic IDs.
- `create()` and registration of a new unidentified Objective assign exactly
  one ID; assignment is rejected after a different ID exists.
- Legacy load is a distinct path and never assigns a missing ID.

### Registry Indexes

- Canonical index: `objective_id -> Objective` for identified records.
- Compatibility index: `goal -> latest registered Objective`.
- Unidentified legacy records are retained separately and remain accessible
  through goal compatibility lookup.
- `get(Objective)` prefers its ID and falls back to goal only when unidentified.
- `get(goal)` preserves latest-by-goal compatibility.
- A new explicit ID lookup is required; ambiguous strings must not be guessed as
  either goal or ID.
- Existing goal-keyed `all()` may remain a compatibility projection during the
  transition, while persistence uses an explicit complete-record iterator that
  does not collapse repeated goals.

### Persistence and Legacy Loading

- New identified Objective records write `objective_id`.
- Existing fields and lifecycle semantics remain unchanged.
- Legacy records without `objective_id` load with `None` and retain their
  original serialized shape unless a separately approved write-forward policy
  says otherwise.
- Saving unrelated new work must not synthesize IDs for legacy records.
- Duplicate non-null IDs are corrupt data and must fail closed; exact error type
  is an implementation decision.
- No identity may be derived from goal, timestamps, position, or content.

## Deferred Propagation

This contract covers Objective identity only. Plan and QueueItem reference
fields, PlanRegistry identity, execution signatures, active-data migration, and
recovery remain separate work orders.
