# DECISION-REQUEST-009 — Queue-Worker Failure Ownership

## Decision Required

Choose how QAOS records a delegated execution failure after DefaultWorker has
started a QueueItem but before successful completion.

## Evidence

WO-073 proves that an escaping Agent exception leaves the live QueueItem
`running`, while durable and reloaded state remains `pending`. The associated
Task remains `pending`. DefaultWorker currently owns successful QueueItem
transitions; QueueManager owns persistence.

## Options

### Option A — Worker Owns State; QueueManager Guarantees Persistence (Recommended)

DefaultWorker conditionally marks its running QueueItem failed when delegated
execution raises and re-raises the original exception. It conditionally fails
an executable Task only when the Task entered `running`; failures before Task
start preserve `pending`. QueueManager guarantees that the resulting state is
saved before the exception escapes.

Consequences:

- keeps execution-state ownership with the component that starts execution;
- keeps durable storage ownership with QueueManager;
- distinguishes never-started Task work from failed Task execution;
- requires a coordinated but bounded contract across two existing layers.

### Option B — QueueManager Owns All Failure Transitions

QueueManager catches worker exceptions, marks the QueueItem and any incomplete
Task failed, saves, and re-raises.

Consequences:

- centralizes queue persistence and failure handling;
- makes QueueManager infer execution semantics owned by Worker and Capability;
- collapses never-started and started Task failures.

### Option C — Preserve Current State

Document live `running` and persisted `pending` as intentional after delegated
failure.

Consequences:

- requires no code change;
- preserves contradictory operational state;
- prevents reliable recovery or retry decisions.

## Recommendation

Select **Option A**. It follows the established ownership pattern: the
execution component owns lifecycle transitions, while the manager owns durable
persistence. The conditional Task rule avoids claiming that work failed when
it never started.

## Explicitly Separate Future Decisions

- persisted exception details;
- retry, resume, rollback, and recovery queues;
- partial-plan continuation;
- worker availability and scheduling;
- provider, model, fallback, and deployment policy.
