# OWNER-DECISION-016 — Task Identity

## Decision

The owner selected **Option A — PlannerManager-Assigned Task IDs** from
DECISION-REQUEST-016.

## Governing Contract

### Identity Ownership

- Task supports an optional immutable opaque `task_id`.
- PlannerManager owns an injected zero-argument Task ID generator and assigns
  identity to new Plan Tasks before persistence or queueing.
- IDs are provider-neutral, carry no semantic meaning, and are unique within the
  planner workspace. Tests may inject deterministic generators.
- Plan remains the canonical owner of its Tasks; QueueItem never generates or
  owns Task identity.

### Plan and Persistence

- Identified new Tasks conditionally serialize `task_id` inside Plan data.
- Plan provides explicit Task lookup by ID; descriptions are never guessed as
  IDs.
- Duplicate non-null Task IDs fail closed before persistence.
- Legacy Tasks without `task_id` load unidentified and retain field omission.
- Saving unrelated work never assigns IDs to loaded legacy Tasks. Migration or
  write-forward requires a separate owner decision.

### Queue Action Reference

- QueueItem carries optional `task_id` copied from its identified Plan Task.
- Its embedded action payload remains compatibility execution state, while
  `task_id` is the canonical correlation reference after reload.
- QueueManager conditionally loads and persists the reference and fails closed
  when an embedded identified action disagrees with it.
- Council QueueItems without Task actions carry no `task_id`.

### Recovery Boundary

- Recovery resolves QueueItem `task_id` against the identified Plan before any
  mutation.
- Missing, duplicate, mismatched, or unidentified recovery references fail
  closed.
- Task identity enables coherent recovery but does not itself implement or
  authorize recovery execution.

## Scope Boundary

This decision authorizes a separate bounded Task identity foundation work order.
It does not authorize recovery, migration, legacy association, QueueItem
identity, automatic retry, retry policy, scheduling, audit evidence,
Kernel/CLI/UI exposure, provider fallback, or unrelated QAOS changes.
