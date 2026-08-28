# FINDING-018 — Execution Engine Global Dependencies

## Status

`RESOLVED — WO-045`

## Evidence

ExecutionEngine directly called module-level planner_manager and queue_manager.
An explicitly composed executive pipeline therefore crossed back into default
workspace state during its execution stage.

## Resolution

WO-045 adds explicit planner and queue injection with the existing managers as
compatibility defaults. Existing execution order and stage ownership are proven.

## Boundary

Worker selection, ExecutionManager registry/objective ownership, and other
pipeline stages remain outside this work order.
