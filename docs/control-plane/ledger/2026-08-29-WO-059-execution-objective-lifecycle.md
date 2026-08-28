# WO-059 — Execution Objective Lifecycle

## Objective

Make ExecutionManager the single owner of canonical Objective execution
lifecycle transitions and persistence.

## Architectural Context

Objective entities are state-only and ObjectiveManager owns persistence.
ExecutionManager already owns the selected ObjectiveManager and surrounds one
ExecutionEngine call, making it the existing non-duplicative lifecycle boundary.

## Requirements

1. Resolve the default engine before beginning lifecycle transitions.
2. Start the Objective before invoking the engine.
3. Complete the Objective after successful engine execution.
4. On engine failure, fail the Objective and re-raise the original exception.
5. Persist each transition only through the selected ObjectiveManager.

## Scope

- ExecutionManager Objective lifecycle coordination
- Success, failure, ordering, persistence, and full-runtime tests
- Finding, verification, current-state, and handoff records

## Explicit Non-Goals

- No transition validation, retry, rollback, or persistence-error policy.
- No other executive layer, schema, provider, model, credential, or Content OS change.

## Verification Requirements

- Prove exact start-engine-complete and start-engine-fail ordering.
- Prove failure re-raises unchanged.
- Prove the full explicit runtime persists a completed Objective.
- Run focused/full tests, import sweep, compilation, architecture inspection,
  and active-data comparison.

## Stop Condition

Stop after FINDING-031 is independently reviewed and WO-059 is published.
