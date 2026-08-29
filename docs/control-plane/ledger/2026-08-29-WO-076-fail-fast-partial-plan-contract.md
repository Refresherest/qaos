# WO-076 — Fail-Fast Partial-Plan Contract

## Objective

Implement OWNER-DECISION-010 by designating and regression-testing the existing
QueueManager fail-fast call behavior.

## Architectural Context

QueueManager already stops at the first worker exception and WO-074 guarantees
durable state. OWNER-DECISION-010 makes that observed behavior authoritative;
no product-code change is required.

## Scope

- Add one regression test with three QueueItems and failure on the second.
- Verify only the first two items are attempted.
- Verify QueueItem and Task states are `completed, failed, pending`.
- Verify persistence and reload match live state.
- Verify the original exception object is preserved.

## Explicit Non-Goals

- No QueueManager, Worker, ExecutionEngine, status-schema, continuation, retry,
  recovery, aggregation, dependency, error-detail, provider, model, credential,
  Content OS, fallback execution, or deployment change.

## Verification Requirements

- Run focused worker, queue, capability, and runtime tests.
- Run full pytest, import sweep, compile, and architecture inspection.
- Verify active data, project-state JSON, secrets, whitespace, and scope.

## Stop Condition

Stop after FINDING-035 is resolved, independently reviewed, recorded, and
pushed.
