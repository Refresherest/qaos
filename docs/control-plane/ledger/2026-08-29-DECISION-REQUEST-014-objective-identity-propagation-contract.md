# DECISION-REQUEST-014 — Objective Identity Propagation Contract

## Decision Required

Choose the Plan and QueueItem Objective-identity propagation and compatibility
contract.

## Options

### Option A — Additive References with Dual Plan Indexes (Recommended)

Plan and QueueItem copy optional `objective_id` from Objective while retaining
goal text. PlanRegistry gains canonical ID lookup, latest-by-goal compatibility,
and complete-record iteration. QueueItems share the non-unique reference.
Legacy missing-reference records pass through without inference.

Consequences:

- distinguishes repeated equal-goal attempts end to end;
- preserves existing goal-string callers and serialized display data;
- keeps ObjectiveManager as the only identity source;
- supports phased implementation before recovery;
- requires bounded changes across Plan, planner, queue, Council, and execution.

### Option B — Replace Goal References with Objective IDs Immediately

Plan and QueueItem persist only Objective IDs and all lookup switches to ID keys.

Consequences:

- makes identity canonical in every downstream representation immediately;
- breaks raw-goal callers, display compatibility, and legacy loading;
- would require migration or inferred association, both currently excluded;
- couples propagation to a disruptive compatibility cutover.

### Option C — Add Storage Fields Without Runtime Lookup Changes

Persist optional `objective_id` but leave PlanRegistry and ExecutionEngine
goal-keyed and leave QueueItem creation paths goal-only.

Consequences:

- minimizes immediate code changes;
- does not prevent equal-goal Plan misselection;
- produces incomplete propagation depending on construction path;
- cannot provide trustworthy attempt correlation for later recovery.

## Recommendation

Select **Option A**. It makes identity authoritative where correlation matters,
retains goal compatibility explicitly, and keeps recovery and migration outside
this work.

## Required Separate Work

- bounded Plan, PlanRegistry, PlannerManager, QueueItem, QueueManager, Council,
  and ExecutionEngine implementation;
- active-data migration or explicit legacy association policy;
- recovery selection and re-execution behavior;
- continuation guards and queue-processing policy enforcement.
