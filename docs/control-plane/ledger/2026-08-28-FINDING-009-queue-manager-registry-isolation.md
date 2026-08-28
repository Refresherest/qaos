# FINDING-009 — Queue Manager Registry Isolation

## Status

`RESOLVED — WO-034`

## Evidence

QueueManager accepted explicit Stores but all instances used and cleared one
module-level queue list. Creating or loading an isolated manager could therefore
replace the queue state used by another workspace or the default manager.

## Resolution

WO-034 introduces instantiable QueueRegistry state. Explicitly stored managers
receive private registries by default; the default manager and compatibility
functions retain the default registry.

## Boundary

Queue processing, worker selection, item schema, statuses, and ordering are not
changed or declared correct by this work order.
