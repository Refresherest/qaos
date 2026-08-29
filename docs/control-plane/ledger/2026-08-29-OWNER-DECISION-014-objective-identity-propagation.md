# OWNER-DECISION-014 — Objective Identity Propagation

## Decision

The owner selected **Option A — Additive References with Dual Plan Indexes**
from DECISION-REQUEST-014.

## Governing Contract

### Shared References

- Plan and QueueItem may copy an optional `objective_id` from Objective; they do
  not generate, assign, mutate, or own it.
- Existing objective goal text remains compatibility and display data.
- Constructors handed an Objective capture its goal and current ID. Raw goal
  strings remain supported and create unidentified downstream records unless a
  trusted loading path supplies an explicit ID.
- Identity is never inferred from goal, timestamps, task text, content, or order.

### Plan Boundary

- Plan conditionally serializes `objective_id`; legacy omission is preserved.
- PlanRegistry maintains canonical `objective_id -> Plan` lookup, a
  `goal -> latest registered Plan` compatibility projection, and complete-record
  iteration that preserves equal-goal Plans.
- Objective-object lookup prefers ID and falls back to goal only when the
  Objective is unidentified. Goal-string lookup remains latest-by-goal.
- Explicit ID lookup is separate; arbitrary strings are never guessed as IDs.
- A different Plan using an already registered non-null `objective_id` fails
  closed because this boundary permits one canonical Plan per Objective.
- ExecutionEngine looks up a Plan using the Objective object, not goal text.

### Queue Boundary

- QueueItem stores optional `objective_id` beside its existing goal string.
- CouncilManager and ExecutionEngine propagate the supplied Objective's ID.
- QueueManager conditionally loads and persists the reference.
- Multiple QueueItems may share one `objective_id`; the reference is not Queue
  identity and creates no uniqueness constraint.

### Legacy Boundary

- Legacy Plan and QueueItem records without `objective_id` load with `None`.
- Loading or unrelated saving never synthesizes a reference.
- Missing fields remain omitted unless a separate migration or explicit legacy
  association policy is approved.

## Scope Boundary

This decision authorizes a separate bounded propagation implementation work
order. It does not authorize active-data migration, legacy association,
recovery selection, re-execution, filtering, continuation guards, queue policy
changes, credentials, provider settings, or unrelated QAOS changes.
