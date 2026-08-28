# FINDING-033 — Pre-Execution Objective Lifecycle

## Status

`OPEN — DECISION REQUIRED`

## Evidence

OperationalSession creates and persists a canonical Objective before invoking
Kernel. ExecutionManager marks failures only after its own `start` transition.
Therefore, an exception in classification, council delegation, or planning can
occur before ExecutionManager owns the lifecycle.

An isolated WO-070 probe replaced the session's Kernel with a deterministic
pre-execution failure. `execute_goal` re-raised `pre-execution failure`, while
the selected workspace persisted:

- one Objective;
- status `pending`;
- `started: null`;
- `completed: null`.

## Impact

The CLI correctly returns an execution-failure status, but persisted workspace
state can describe the same attempt as pending indefinitely. This weakens
operator recovery and makes failed versus never-started work ambiguous.

## Existing Boundary

ExecutionManager already owns `start -> complete/fail` once execution begins.
Any change must preserve that ownership and decide who owns failure before
ExecutionManager is reached.

## Scope Boundary

WO-070 is characterization only. Resolve lifecycle ownership through an owner
decision before changing OperationalSession, Executive, or ObjectiveManager.
