# FINDING-030 — Default Worker Leaves Queue Items Pending

## Status

`RESOLVED — WO-057`

## Evidence

An isolated default QueueManager execution completed its Task through the
built-in Agent, planning Skill, and SystemCapability, but the QueueItem remained
`pending` with no timestamps or result after persistence. The canonical Worker
contract marks successfully executed items running and then completed.

## Resolution

WO-057 gives DefaultWorker the established successful QueueItem lifecycle. It
sets running/completed timestamps, supplies the canonical completion result only
when the delegated Agent did not supply one, and preserves the delegated return.

## Boundary

Failure transitions, retry policy, worker availability, capability behavior,
queue ordering, and schemas are unchanged.
