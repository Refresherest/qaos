# FINDING-036 — Later-Call Implicit Continuation

## Status

`OPEN — OWNER DECISION REQUIRED`

## Evidence

OWNER-DECISION-010 governs one failed QueueManager processing call only. The
public `process()` method selects every pending QueueItem and has no attempt,
batch, or failed-Objective guard.

An isolated WO-077 probe first produced the designated fail-fast state:

- calls: first item, second item;
- QueueItems: `completed, failed, pending`;
- second item raised `second task failure`.

Calling the same QueueManager's ordinary `process()` method again then:

- skipped the failed second item;
- executed the previously unattempted third item;
- persisted QueueItems and Tasks as `completed, failed, completed`.

## Impact

An ordinary queue-processing call can become a recovery/continuation mechanism
without an explicit recovery decision. QueueItem carries an objective goal
string but no attempt or batch identity, so the queue cannot robustly
distinguish a failed plan's remainder from unrelated pending work.

## Existing Boundary

WO-076 authorizes fail-fast semantics within one call and explicitly excludes
later-call behavior. ExecutionEngine is the only product caller, but
QueueManager.process remains publicly callable and drains all pending work.

## Scope Boundary

WO-077 is characterization only. Resolve later-call continuation through
DECISION-REQUEST-011 before changing QueueManager, QueueItem identity,
ExecutionEngine, or recovery behavior.
