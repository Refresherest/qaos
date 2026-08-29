# WO-075 — Partial-Plan Disposition Assessment

## Objective

Characterize queue and Task disposition when one item fails after earlier work
completed and before later work starts.

## Scope

- Inspect QueueManager, DefaultWorker, ExecutionEngine, and ExecutionManager
  failure boundaries.
- Run one isolated three-item queue probe with failure on the second item.
- Record the exact live, persisted, and reloaded state.
- Record one bounded finding and owner-decision boundary.
- Remove the disposable probe workspace.

## Explicit Non-Goals

- No product code, tests, status schema, continuation, aggregation, retry,
  recovery, rollback, persisted-error, provider, model, credential, Content OS,
  fallback execution, or deployment change.

## Verification Requirements

- Verify attempted-item order and every QueueItem and Task state.
- Verify live, persisted, and reloaded state agree.
- Confirm active data remains unchanged and remove the probe workspace.
- Validate project-state JSON, whitespace, secret, and scope boundaries.

## Stop Condition

Stop after the assessment, finding, decision request, verification, and handoff
are recorded and pushed. Do not select a partial-plan policy.
