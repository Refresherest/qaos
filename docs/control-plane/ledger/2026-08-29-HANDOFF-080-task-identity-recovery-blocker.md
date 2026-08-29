# HANDOFF-080 — Task Identity Recovery Blocker

## Branch and Baseline

- Branch: `feat/operational-builder-chain`
- Input baseline: `2cdc477`
- Work order: WO-089

## Outcome

Recovery implementation stopped before product-code changes because durable Task
correlation is absent. After reload, Plan Task and QueueItem action are separate
objects; resetting the queue copy leaves the Plan copy failed.

## Proven Evidence

- `SAME_OBJECT False`
- Plan Task remained `failed`
- Queue action changed from `failed` to `pending`
- Probe data was isolated and removed
- Active runtime data remained unchanged

## Architectural Consequence

Implementing recovery now would either create split-brain Plan/Queue state,
limit recovery to one live process, or infer Task identity from unreliable data.
All three violate the approved contract or QAOS identity rules.

## Decision Required

Select Option A, B, or C in DECISION-REQUEST-016. Option A—PlannerManager-owned
opaque Task IDs with QueueItem references—is recommended.

OWNER-DECISION-015 recovery implementation remains blocked until this decision
and its separate Task identity foundation are complete.
