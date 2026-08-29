# OWNER-DECISION-011 — Explicit Recovery Boundary

## Decision

The owner selected **Option A — Explicit Recovery Boundary with Attempt
Identity** from DECISION-REQUEST-011.

## Architectural Direction

1. Ordinary `QueueManager.process()` is routine execution, not an authorized
   recovery operation.
2. A failed execution attempt's pending remainder must not be intentionally
   continued until QAOS can identify that attempt canonically.
3. Recovery must use an explicit, separately authorized boundary rather than a
   repeated ordinary queue call.
4. A naive global failed-plus-pending guard is not authorized because it can
   block unrelated work.
5. Current repeat-call behavior remains unapproved compatibility behavior
   pending design and must not be exposed or invoked as recovery.

## Required Design Before Implementation

- canonical attempt/batch identity and owner;
- propagation through Objective, Plan, QueueItem, and execution boundaries;
- persisted representation and compatibility/migration behavior;
- relationship between one attempt and one Objective execution;
- explicit recovery authorization and selection semantics.

## Exclusions

This decision does not authorize entity or schema changes, migration, recovery
APIs, retry, continuation guards, dependency inference, error persistence,
provider/model fallback, or deployment changes.
