# PROPOSAL-007 — Objective Identity Propagation Contract

## Evidence Summary

- Plan converts an Objective to goal text and persists only `objective`.
- PlanRegistry is one goal-keyed dictionary, so equal-goal Plans collapse.
- ExecutionEngine looks up Plans by `objective.goal`, even when an identified
  Objective is available.
- CouncilManager and ExecutionEngine construct QueueItems from goal text.
- QueueItem and QueueManager persist no Objective identity reference.
- A Plan is one planned representation for an Objective; multiple QueueItems
  may legitimately reference the same Objective and Plan.
- Active and legacy Plan and QueueItem records contain goal strings only.

## Recommended Contract

### Shared Reference Semantics

- Plan and QueueItem may carry optional `objective_id` references copied from an
  Objective; neither generates, assigns, or owns identity.
- Existing `objective` goal text remains compatibility and display data.
- Constructors handed an Objective capture its goal and current ID. Constructors
  handed a raw goal string remain supported and produce an unidentified
  downstream record unless an explicit ID is supplied during trusted loading.
- No reference is derived from goal, timestamps, task text, ordering, or content.

### Plan and PlanRegistry

- Plan serializes `objective_id` only when present; `to_dict` and `from_dict`
  follow the same conditional legacy behavior as PlannerManager persistence.
- PlanRegistry maintains canonical `objective_id -> Plan` lookup for identified
  Plans and a `goal -> latest registered Plan` compatibility projection.
- Complete-record iteration preserves Plans for repeated equal-goal Objectives;
  goal-keyed `all()` may remain a compatibility projection.
- `get(Objective)` prefers its ID and falls back to goal only when the Objective
  is unidentified. `get(goal)` remains latest-by-goal. Explicit ID lookup is a
  separate API; arbitrary strings are never guessed to be IDs.
- A different Plan using an already registered non-null `objective_id` fails
  closed because one Objective has one canonical Plan in this boundary.
- ExecutionEngine passes the Objective object to Plan lookup so identified
  invocations cannot select another equal-goal Objective's Plan.

### QueueItem and QueueManager

- QueueItem stores optional `objective_id` alongside its existing goal string.
- CouncilManager and ExecutionEngine propagate the supplied Objective's ID when
  creating QueueItems.
- QueueManager conditionally persists and loads `objective_id`.
- Queue identity is not unique by `objective_id`: every task item for one
  Objective shares the same reference.
- This work adds no recovery selector, filtering API, queue guard, or processing
  semantic. Those require a later recovery work order.

### Legacy and Write Behavior

- Legacy Plan and QueueItem records missing `objective_id` load with `None`.
- Loading or saving unrelated work never synthesizes their identity.
- Legacy records retain omission of the field unless a separately approved
  migration or explicit association policy is selected.
- Identified new records write the reference; unidentified compatibility-created
  records continue to omit it.

## Deferred Work

Active-data migration, association of legacy records, recovery selection,
re-execution, continuation guards, and queue processing remain separate work.
