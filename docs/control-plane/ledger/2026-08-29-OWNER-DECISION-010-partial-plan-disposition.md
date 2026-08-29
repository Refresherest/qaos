# OWNER-DECISION-010 — Partial-Plan Disposition

## Decision

The owner selected **Option A — Explicit Fail-Fast Call Boundary** from
DECISION-REQUEST-010.

## Authorized Contract

When one QueueItem fails during a QueueManager processing call:

1. processing stops at that first failure;
2. already-completed work remains completed;
3. the failed item and any started Task retain failed state;
4. later never-attempted work remains pending;
5. all state is persisted before the original exception escapes;
6. no continuation occurs within that failed processing call.

## Exclusions

This decision does not authorize a recovery or retry entry point, a subsequent
processing call, error aggregation, dependency inference, blocked/cancelled
statuses, persisted error details, provider/model fallback, or deployment
policy.
