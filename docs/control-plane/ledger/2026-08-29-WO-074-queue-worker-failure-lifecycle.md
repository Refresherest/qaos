# WO-074 — Queue-Worker Failure Lifecycle

## Objective

Implement OWNER-DECISION-009 and resolve FINDING-034 without moving lifecycle
or persistence ownership outside the established Worker and QueueManager
boundaries.

## Architectural Context

DefaultWorker owns QueueItem execution state. Delegated execution owns whether
a Task starts. QueueManager owns durable queue persistence.

## Scope

- Catch exceptions escaping Agent execution in DefaultWorker.
- Fail only a still-running QueueItem and record its completion timestamp.
- Fail only an associated executable that is running and supports `fail()`.
- Preserve a never-started Task as pending.
- Re-raise the original exception.
- Guarantee QueueManager saves state when processing exits through an
  exception.

## Explicit Non-Goals

- No error-detail schema, retry, resume, rollback, recovery, partial-plan,
  scheduling, provider, model, credential, Content OS, fallback execution, or
  deployment change.
- No change to Agent, Skill, Capability, Task, QueueItem, or generic Worker
  public contracts.

## Verification Requirements

- Test failure before Task start and after Task start.
- Verify exact exception identity, live state, timestamps, and persisted state.
- Run focused tests, full pytest, import sweep, compile, and architecture
  inspection.
- Verify active data, project-state JSON, secrets, whitespace, and scope.

## Stop Condition

Stop after FINDING-034 is resolved, independently reviewed, recorded, and
pushed.
