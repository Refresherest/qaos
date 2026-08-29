# DECISION-REQUEST-016 — Task Identity Contract

## Decision Required

Choose how durable recovery correlates a QueueItem action with its canonical
Plan Task after persistence reload.

## Options

### Option A — PlannerManager-Assigned Task IDs (Recommended)

PlannerManager assigns immutable opaque IDs to new Plan Tasks before persistence
or queueing. QueueItem copies the Task ID as a non-owning action reference.
Legacy missing-ID Tasks remain unidentified without inference.

Consequences:

- creates durable, deterministic Task correlation;
- keeps Plan as the canonical Task owner;
- permits coherent Plan and Queue recovery after restart;
- preserves legacy data truthfully;
- requires a bounded Task identity foundation before recovery implementation.

### Option B — Live-Process-Only Recovery

Recovery relies on Plan and QueueItem sharing the same in-memory Task object and
is unavailable after reload.

Consequences:

- avoids schema changes;
- makes recovery disappear across restart, exactly when persisted recovery is
  most important;
- creates environment-dependent semantics;
- does not satisfy OWNER-DECISION-015's durable state contract.

### Option C — Infer Task Correlation

Match QueueItem actions to Plan Tasks by description, list position, timestamps,
or a combination of those fields.

Consequences:

- avoids explicit Task identity;
- conflates descriptive/mutable data with canonical identity;
- fails with repeated task descriptions or reordered records;
- violates QAOS's established prohibition on inferred legacy identity.

## Recommendation

Select **Option A**. It extends the existing manager-owned identity pattern to
the canonical Plan Task boundary and makes recovery coherent after reload.

## Required Separate Work

- bounded Task identity and QueueItem action-reference implementation;
- OWNER-DECISION-015 recovery implementation after identity is verified;
- any legacy Task migration or association policy;
- public recovery exposure, retry policy, scheduling, and audit evidence.
