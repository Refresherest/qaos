# PROPOSAL-009 — Task Identity Contract

## Evidence Summary

- Objective ID identifies one operational invocation.
- A Plan owns an ordered list of Task records but Tasks have no identity.
- Each QueueItem embeds a second serialized Task copy as its action.
- Shared in-memory object identity is lost when PlannerManager and QueueManager
  reload independently.
- Durable recovery must update the canonical Plan Task and queued execution
  state coherently without descriptive or positional inference.

## Recommended Contract

### Identity Ownership

- Task gains an optional immutable opaque `task_id`.
- PlannerManager owns an injected zero-argument Task ID generator and assigns IDs
  to new Plan Tasks before they are persisted or queued.
- Task identity is unique within the planner workspace and carries no provider
  or semantic meaning.
- Tests inject deterministic IDs.

### Plan and Persistence

- Identified new Task records conditionally persist `task_id` inside Plan data.
- Plan provides explicit Task lookup by ID; arbitrary descriptions are never
  guessed as IDs.
- Duplicate non-null Task IDs fail closed before persistence.
- Legacy Tasks missing `task_id` load unidentified and retain field omission.
- PlannerManager saving unrelated work never assigns identity to loaded legacy
  Tasks; any write-forward or migration policy requires separate approval.

### Queue Action Reference

- QueueItem carries optional `task_id` copied from its identified Plan Task.
- The embedded action payload retains compatibility state, but `task_id` is the
  canonical correlation reference after reload.
- QueueManager conditionally loads and persists the reference and verifies that
  an embedded identified action agrees with the QueueItem reference.
- Council QueueItems without Task actions carry no `task_id`.

### Recovery Use

- ExecutionEngine resolves each selected QueueItem `task_id` against the
  identified Plan before any mutation.
- Missing, duplicate, mismatched, or unidentified Task references fail closed.
- Recovery resets both the selected QueueItem action and its canonical Plan Task
  explicitly, preserving coherent persistence across reload.

## Deferred Work

Task identity implementation is separate from recovery implementation. Active
legacy migration, association, QueueItem identity, automatic retry, Kernel/CLI
exposure, scheduling, and audit evidence remain excluded.
