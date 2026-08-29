# OWNER-DECISION-015 — Explicit Recovery

## Decision

The owner selected **Option A — Retry Failed Item, Then Pending Remainder** from
DECISION-REQUEST-015.

## Governing Contract

### Selection and Preconditions

- ExecutionManager owns an explicit recovery operation selected only by
  canonical `objective_id`; goal strings are not accepted or guessed as IDs.
- ObjectiveManager resolves the ID. The Objective must be identified and failed,
  with an identified Plan and QueueItems carrying the exact same ID.
- Missing or inconsistent Objective, Plan, QueueItems, or failure state fails
  closed before mutation.
- Legacy unidentified records remain non-recoverable without separately approved
  association or migration.

### Eligible Work

- The attempt must contain exactly one failed QueueItem.
- Recovery targets that failed item and every later pending item with the same
  Objective ID, in persisted queue order.
- Completed items remain completed and are never re-executed.
- Pending items before the failure or multiple failed items fail closed.
- Unrelated Objective IDs remain untouched.

### Reset, Execution, and Lifecycle

- Immediately before retry, only the failed QueueItem and its failed Task reset
  to pending; their result and execution timestamps are cleared.
- Existing pending remainder retains its state until executed.
- DefaultWorker executes the selected sequence in order with fail-fast behavior.
- Queue state persists in `finally`, and an escaping original exception is
  preserved.
- ExecutionManager moves the Objective to running before retry, completes it only
  after every selected item completes, and fails it if recovery raises.
- Planner state is saved after successful Task transitions.
- Recovery does not re-run classification, Council delegation, or planning and
  does not create QueueItems.

### Ordinary Processing Separation

- Ordinary QueueManager processing remains routine execution.
- Pending identified items are skipped when that same Objective ID already has a
  failed QueueItem.
- Pending unrelated Objective IDs remain eligible; no global failed-plus-pending
  guard is introduced.
- No goal grouping is inferred for unidentified legacy records.

## Scope Boundary

This decision authorizes a separate bounded implementation work order for the
internal recovery boundary and ordinary-processing guard only. It does not
authorize migration, legacy association, automatic retry, retry budgets,
backoff, scheduling, audit records, Kernel/CLI/UI exposure, provider fallback,
or unrelated QAOS changes.
