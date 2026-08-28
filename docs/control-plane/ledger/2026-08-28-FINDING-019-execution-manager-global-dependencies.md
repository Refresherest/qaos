# FINDING-019 — Execution Manager Global Dependencies

## Status

`RESOLVED — WO-046`

## Evidence

ExecutionManager resolved the default engine through module registry functions
and always saved through the default ObjectiveManager. An explicit execution
stage could not retain isolated engine or persistence ownership.

## Resolution

WO-046 introduces instantiable ExecutionRegistry state and explicit registry and
ObjectiveManager injection, retaining existing defaults and execution-save order.

## Boundary

ExecutionEngine behavior, worker selection, objective lifecycle transitions,
and other executive stages remain outside this work order.
