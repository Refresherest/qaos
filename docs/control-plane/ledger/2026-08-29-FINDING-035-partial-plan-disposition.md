# FINDING-035 — Partial-Plan Disposition

## Status

`OPEN — OWNER DECISION REQUIRED`

## Evidence

QueueManager processes pending items sequentially and propagates the first
worker exception. WO-074 now guarantees that state is durably saved at that
boundary.

An isolated WO-075 probe added three QueueItems with Tasks and made delegated
execution fail on the second item. The probe observed:

- attempted objectives: first, then second;
- QueueItems: `completed, failed, pending`;
- Tasks: `completed, failed, pending`;
- persisted state: identical;
- reloaded state: identical;
- third item: not attempted.

## Impact

The stored state accurately describes the interrupted batch, but QAOS has no
governing policy stating whether later independent work should remain pending,
continue after the failure, or receive a terminal disposition. That choice
affects execution guarantees and future recovery behavior.

## Existing Boundary

QueueManager currently has fail-fast call semantics. ExecutionManager fails the
Objective when ExecutionEngine propagates the exception. Neither boundary is
authorized to infer what should happen to later unattempted Tasks.

## Scope Boundary

WO-075 is characterization only. Resolve partial-plan disposition through
DECISION-REQUEST-010 before changing QueueManager, ExecutionEngine, Task, or
QueueItem behavior. Retry and recovery remain separate decisions.
