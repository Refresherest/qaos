# DECISION-REQUEST-015 — Explicit Recovery Contract

## Decision Required

Choose the failed-attempt recovery and ordinary-processing separation contract.

## Options

### Option A — Retry Failed Item, Then Pending Remainder (Recommended)

An explicit Objective-ID recovery operation resets and retries the single failed
item, then processes that attempt's later pending items in order. Completed and
unrelated items remain untouched. Ordinary processing skips pending items only
for identified attempts that already contain failure.

Consequences:

- produces a coherent completed attempt when recovery succeeds;
- preserves completed work and avoids duplicate side effects;
- prevents ordinary calls from silently continuing failed identified attempts;
- keeps unrelated attempts processable;
- requires strict precondition, reset, lifecycle, and persistence tests.

### Option B — Continue Pending Remainder Without Retrying Failure

Recovery leaves the failed QueueItem and Task failed and executes only later
pending items.

Consequences:

- minimizes re-execution;
- leaves the attempt and Plan internally failed even after the remainder runs;
- cannot coherently complete the Objective;
- treats continuation as recovery without resolving the failed unit.

### Option C — Restart the Entire Attempt

Recovery resets every completed, failed, and pending item for the Objective ID
and executes the whole attempt again.

Consequences:

- produces a clean full rerun model;
- repeats already completed actions and risks duplicate side effects;
- discards verified progress;
- requires idempotency contracts that QAOS does not currently have.

## Recommendation

Select **Option A**. It repairs the failed unit, preserves prior completed work,
continues only the identified remainder, and creates a precise boundary between
ordinary execution and explicit recovery.

## Required Separate Work

- bounded QueueManager, ExecutionEngine, and ExecutionManager recovery
  implementation plus ordinary-processing guard;
- public Kernel/CLI recovery authorization, if desired;
- legacy association or migration policy;
- retry budgets, scheduling, audit evidence, and historical-state repair.
