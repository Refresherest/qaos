# FINDING-034 — Queue-Worker Failure Lifecycle

## Status

`OPEN — OWNER DECISION REQUIRED`

## Evidence

DefaultWorker marks a QueueItem `running` before resolving and invoking its
Agent. It marks the item completed only after Agent execution returns.
QueueManager persists queue state only after its complete processing loop
returns.

An isolated WO-073 probe used an explicit workspace and an Agent that raised
`delegated worker failure`. The exception propagated, and the observed state
was:

- live QueueItem: `running`;
- live Task: `pending`;
- persisted QueueItem: `pending`;
- persisted Task: `pending`;
- reloaded QueueItem: `pending`;
- reloaded Task: `pending`.

## Impact

One failed attempt has two different queue states depending on whether an
operator observes the live process or reloads the workspace. Neither state
records failure. This weakens failure diagnosis and makes later recovery or
retry policy unsafe to define.

## Existing Boundary

DefaultWorker owns the QueueItem running/completed transitions. Task lifecycle
is delegated through Agent, Skill, and Capability. QueueManager owns durable
queue persistence. A repair therefore requires an explicit decision about
state-transition and persistence responsibilities across those boundaries.

## Scope Boundary

WO-073 is characterization only. Resolve ownership through
DECISION-REQUEST-009 before changing Worker, QueueManager, Task, Agent, Skill,
or Capability behavior. Retry and recovery remain separate decisions.
