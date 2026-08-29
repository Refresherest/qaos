# HANDOFF-079 — Explicit Recovery Decision

## Branch and Baseline

- Branch: `feat/operational-builder-chain`
- Input baseline: `c1203eb`
- Work order: WO-088

## Completed

OWNER-DECISION-015 records the owner's selection of Option A. Explicit recovery
will select a failed Objective by canonical ID, retry its one failed QueueItem,
then execute that attempt's later pending remainder without repeating completed
or unrelated work.

Ordinary processing will skip only pending items whose identified attempt
already has failure, while unrelated attempts remain eligible.

## Verified Boundary

This checkpoint changes control-plane documentation only. Product code, tests,
APIs, schemas, active data, migration, recovery, automatic retry, retry policy,
Kernel/CLI/UI exposure, credentials, providers, and unrelated files remain
unchanged.

## Open Finding

FINDING-036 remains open until the internal explicit recovery boundary and
attempt-scoped ordinary-processing guard are implemented and verified.

## Next Work Package

Implement only OWNER-DECISION-015 across QueueManager, ExecutionEngine, and
ExecutionManager with focused and regression verification. Do not add migration,
legacy association, automatic retry, retry budgets, scheduling, audit evidence,
or public Kernel/CLI/UI exposure.
