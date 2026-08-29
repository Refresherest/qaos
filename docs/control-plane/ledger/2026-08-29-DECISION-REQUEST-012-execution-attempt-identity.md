# DECISION-REQUEST-012 — Execution-Attempt Identity

## Status

`RESOLVED — OWNER-DECISION-012`

## Decision Required

Choose the canonical owner of execution-attempt identity.

## Options

### Option A — Objective Identity Is Attempt Identity (Recommended)

Add immutable opaque identity to Objective and reference it from Plan and
QueueItem. Preserve goal text only as compatibility/display data.

Consequences:

- reuses the existing lifecycle-bearing source-of-truth concept;
- distinguishes repeated equal goals;
- avoids a duplicate execution lifecycle aggregate;
- requires registry, JSON compatibility, and propagation work;
- establishes one Objective as one operational invocation.

### Option B — Separate ExecutionAttempt Aggregate

Create a new execution-domain entity and storage collection linked to
Objective, Plan, and QueueItem.

Consequences:

- separates goal intent from execution history explicitly;
- supports multiple attempts per Objective naturally;
- duplicates status/timestamps already owned by Objective unless that existing
  lifecycle is redesigned;
- creates a new manager, registry, storage collection, and reconciliation
  boundary.

### Option C — Queue-Local Batch Identity

Add a batch ID only to QueueItem records and let QueueManager own it.

Consequences:

- smallest local schema change;
- cannot canonically identify pre-queue or failed Objective execution;
- makes a downstream projection the source of truth;
- does not satisfy OWNER-DECISION-011 end to end.

## Recommendation

Select **Option A**. Objective already owns the lifecycle of one normal
OperationalSession invocation. Giving it canonical identity extends the
existing concept instead of creating a parallel attempt system.

## Required Separate Implementation Decisions

- ID type and injection contract;
- ObjectiveRegistry canonical and compatibility lookup behavior;
- PlanRegistry handling of repeated goal text;
- legacy load/write-forward and migration policy;
- exact propagation signatures;
- recovery API and re-execution policy.
