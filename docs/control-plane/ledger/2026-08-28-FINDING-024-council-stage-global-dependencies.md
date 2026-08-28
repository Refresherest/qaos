# FINDING-024 — Council Stage Global Dependencies

## Status

`RESOLVED — WO-051`

## Evidence

ExecutivePipeline accepted an explicit CouncilManager, but CouncilManager used
the module council registry, Delegator, and QueueManager. Delegator then used the
module council registry and ObjectiveManager. An explicit executive chain could
therefore assign and enqueue against default workspace state.

## Resolution

WO-051 introduces instantiable CouncilRegistry state and explicit collaborator
selection through CouncilManager and Delegator. Default constructors retain the
existing registered council and managers.

## Boundary

Council membership, routing policy, assignment semantics, queue processing,
objective schema, and lifecycle event subscription are unchanged.
