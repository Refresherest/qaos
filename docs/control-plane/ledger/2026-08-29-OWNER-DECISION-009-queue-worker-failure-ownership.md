# OWNER-DECISION-009 — Queue-Worker Failure Ownership

## Decision

The owner selected **Option A — Worker Owns State; QueueManager Guarantees
Persistence** from DECISION-REQUEST-009.

## Authorized Contract

When delegated execution raises after DefaultWorker starts a QueueItem:

1. DefaultWorker conditionally transitions its still-running QueueItem to
   failed and records completion time.
2. If the associated executable Task entered running, DefaultWorker fails it.
3. A Task that never started remains pending.
4. The original exception is re-raised unchanged.
5. QueueManager persists the resulting queue and Task state before the
   exception escapes its processing boundary.

## Exclusions

This decision does not authorize persisted exception details, retry, resume,
rollback, recovery queues, partial-plan continuation, worker scheduling,
provider/model fallback, or deployment policy.
