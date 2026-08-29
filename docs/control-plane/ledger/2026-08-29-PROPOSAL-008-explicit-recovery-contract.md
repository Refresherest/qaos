# PROPOSAL-008 — Explicit Recovery Contract

## Evidence Summary

- One Objective ID now correlates Objective, Plan, and all QueueItems for an
  operational invocation.
- QueueManager.process selects every pending item and skips failed items.
- A second ordinary call therefore continues an identified attempt's pending
  remainder unless guarded.
- DefaultWorker owns QueueItem and Task execution-state transitions and preserves
  the original exception on failure.
- ExecutionManager owns Objective running/completed/failed transitions.
- The approved fail-fast state has one failed item followed by pending remainder;
  completed items may precede it.

## Recommended Contract

### Explicit Boundary and Selection

- ExecutionManager exposes an explicit recovery operation selected by canonical
  `objective_id`; goal strings are never accepted or guessed as attempt IDs.
- ObjectiveManager resolves the ID. Recovery requires an identified Objective in
  `failed` state, its identified Plan, and QueueItems with the exact same ID.
- Unidentified legacy Objective, Plan, or QueueItem records are non-recoverable
  unless a separate explicit association or migration policy is approved.
- Missing Objective, Plan, QueueItems, failed item, or inconsistent references
  fail closed before any state mutation.

### Eligibility and Ordering

- The approved fail-fast shape contains exactly one failed QueueItem for the
  attempt. More than one failed item is ambiguous and fails closed.
- Recovery targets that failed item and every later pending QueueItem for the
  same Objective ID, in persisted queue order.
- Completed items remain completed and are never re-executed.
- Pending items before the failed item are inconsistent with fail-fast ordering
  and cause recovery to fail closed.
- QueueItems belonging to other Objective IDs remain untouched.

### Reset and Execution

- Immediately before retry, only the selected failed QueueItem and its failed
  Task reset to `pending`; their result and execution timestamps are cleared.
- Existing pending remainder remains pending without timestamp mutation.
- Execution reuses DefaultWorker in order and remains fail-fast.
- Queue state persists in a `finally` boundary and the original exception is
  preserved if recovery fails again.
- ExecutionManager changes the Objective from failed to running before worker
  execution, completes it only after every targeted item completes, and fails it
  again if an exception escapes.
- Planner state is saved after successful task-state transitions.

### Ordinary Processing Separation

- Ordinary `QueueManager.process()` remains routine processing.
- Before executing a pending identified item, it checks whether that same
  Objective ID has a failed QueueItem. If so, it skips that attempt's pending
  items rather than treating the call as recovery.
- Pending items for unrelated Objective IDs remain eligible, avoiding the
  forbidden global failed-plus-pending guard.
- No goal-based grouping is inferred for unidentified legacy items. They remain
  outside authorized recovery and require separate compatibility policy.

### Explicit Exclusions

- Recovery is manually invoked; there is no automatic retry.
- No retry count, backoff, scheduling, CLI, Kernel, UI, or provider fallback is
  introduced.
- Recovery does not re-run classification, Council delegation, or planning and
  does not create duplicate QueueItems.

## Deferred Work

Legacy association/migration, public Kernel or CLI authorization, retry budgets,
scheduling, recovery audit records, and recovery of inconsistent historical
states remain separate work orders.
