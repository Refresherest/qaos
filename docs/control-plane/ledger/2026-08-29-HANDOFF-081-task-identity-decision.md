# HANDOFF-081 — Task Identity Decision

## Branch and Baseline

- Branch: `feat/operational-builder-chain`
- Input baseline: `5a086b2`
- Work order: WO-090

## Completed

OWNER-DECISION-016 records the owner's selection of Option A. PlannerManager
will assign immutable opaque IDs to new Plan Tasks before persistence or
queueing. QueueItem will carry the ID as a non-owning action reference, and
legacy missing-ID Tasks will remain unidentified without inference.

## Verified Boundary

This checkpoint changes control-plane documentation only. Product code, tests,
APIs, schemas, active data, recovery, migration, legacy association, retry
policy, public exposure, credentials, providers, and unrelated files remain
unchanged.

## Open Findings

- FINDING-037 remains open until Task identity is implemented and reload-tested.
- FINDING-036 remains open; explicit recovery implementation is still blocked by
  FINDING-037.

## Next Work Package

Implement only OWNER-DECISION-016 across Task, Plan, PlannerManager, QueueItem,
QueueManager, and the queue-construction path with focused and regression tests.
Do not implement recovery, migration, legacy association, QueueItem identity,
automatic retry, audit evidence, or Kernel/CLI/UI exposure.
