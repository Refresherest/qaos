# FINDING-025 — Queue Worker Global Dependency

## Status

`RESOLVED — WO-052`

## Evidence

QueueManager supported isolated Stores and registry state, but `process()`
always resolved the default worker through the module worker_manager. An
explicit execution chain could not select its worker service without replacing
module state.

## Resolution

WO-052 allows QueueManager to retain a caller-selected worker service while
preserving the module worker_manager as the default compatibility path.

## Boundary

Worker registry lifecycle, worker selection policy, agent execution, queue
ordering, item schema, and error behavior are unchanged.
