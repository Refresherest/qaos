# FINDING-026 — Worker-to-Agent Global Dependencies

## Status

`RESOLVED — WO-053`

## Evidence

QueueManager could select a WorkerManager, but WorkerManager used one module
worker registry and module DefaultWorker. DefaultWorker then resolved the module
AgentManager, whose operations used one module agent registry. An explicit queue
chain could not retain isolated worker and agent ownership.

## Resolution

WO-053 introduces instantiable worker and agent registries plus explicit service
selection through WorkerManager, DefaultWorker, and AgentManager. Default
constructors retain the established module services and registrations.

## Boundary

Agent skill resolution, worker policy, execution semantics, queue schema, and
provider/model behavior are unchanged.
