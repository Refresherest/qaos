# HANDOFF-070 — Execution-Attempt Identity Design

## Work Order

`WO-079`

## Status

`COMPLETE — ACCEPTED WITH NOTES`

## Result

PROPOSAL-005 defines three execution-attempt identity alternatives. No product
code or schema changed.

## Recommendation

Select **Option A — Objective Identity Is Attempt Identity**. Objective already
owns the lifecycle of one normal OperationalSession invocation; Plan and
QueueItem should reference it rather than becoming identity authorities.

## Decision Options

- Option A: immutable Objective identity referenced downstream — recommended
- Option B: separate ExecutionAttempt aggregate and storage
- Option C: QueueItem-local batch identity

## Critical Compatibility Rule

Legacy records without identity must remain unassigned. Do not correlate them
by goal text, timestamp, ordering, or Task descriptions.

## Verification

- Active identity and persistence path: inspected
- Duplicate-concept and source-of-truth risks: recorded
- Product code and tests: unchanged
- Active data: unchanged
- Reviewer: ACCEPT WITH NOTES

## Next Executable Step

Obtain the owner's selection for DECISION-REQUEST-012. Record the selected
identity owner before any registry, schema, or propagation implementation.

## Stop Condition

WO-079 is complete. Stop pending owner decision.
