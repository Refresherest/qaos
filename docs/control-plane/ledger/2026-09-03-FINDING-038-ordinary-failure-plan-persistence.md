# FINDING-038 — Ordinary Failure Leaves Stale Persisted Plan

## Status

OPEN — blocks recovery after an ordinary execution failure and workspace reload.

## Evidence

At baseline 1ffce3a, run:

`.venv\Scripts\python.exe docs/control-plane/ledger/wo096_recovery_probe.py`

The probe runs execute_goal with a process-local failure on the second Task's
completion, removes that injection, and creates a fresh session for recovery.

- Objective: failed.
- Queue actions: completed, failed, pending, pending, pending.
- Persisted Plan Tasks: pending, pending, pending, pending, pending.
- Recovery: `ValueError: Plan and Queue recovery statuses do not match`.
- State after rejected recovery: unchanged.
- Active-data fingerprints unchanged; disposable workspace removed.

## Cause

ExecutionEngine.execute calls planner.save only after queue.process returns.
When queue processing raises, Queue persists its state but the Plan save is
skipped. The recovery preflight correctly rejects these inconsistent copies.

## Prior Evidence Limitation

WO-092 and WO-095 tests demonstrate recovery from manually prepared coherent
persisted states. They do not prove that ordinary failed execution produces
such a state. The application method exists and its delegation is verified;
end-to-end failure-to-reload recovery is not yet operational.

## Proposed Bounded Repair

Persist canonical Plan Task transitions when ordinary queue execution fails,
preserving the original exception and existing lifecycle ownership. Add an
integration regression that produces a real failure, reloads, and recovers.
Do not weaken recovery preflight or repair historical active data. This finding
is evidence, not authorization to implement outside a separate work order.
