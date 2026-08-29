# DECISION-REQUEST-013 — Objective Identity Contract

## Decision Required

Choose the Objective ID generation, registry compatibility, and legacy loading
contract.

## Options

### Option A — Manager-Injected IDs with Dual Indexes (Recommended)

ObjectiveManager assigns opaque IDs through an injectable generator. Registry
maintains canonical ID lookup and a latest-by-goal compatibility projection.
Legacy missing-ID records remain unassigned and pass through without inference.

Consequences:

- preserves deterministic tests and source-of-truth ownership;
- retains current goal lookup while preserving repeated equal-goal records;
- supports fail-closed duplicate-ID validation;
- requires explicit complete-record iteration for persistence;
- allows phased implementation before downstream propagation.

### Option B — Objective Self-Generates IDs and Registry Switches Immediately

Every Objective constructor creates an ID, and ObjectiveRegistry changes its
public dictionary to ID keys immediately.

Consequences:

- makes all new instances identified automatically;
- introduces nondeterminism into the entity unless generation is also injected;
- risks assigning fabricated IDs while loading legacy data;
- breaks current goal-keyed callers and tests in one step.

### Option C — Deterministic IDs Derived from Existing Fields

Derive identity from goal text plus timestamps or record position.

Consequences:

- avoids storing a generated random ID initially;
- conflates identity with mutable/descriptive data;
- encourages forbidden legacy inference;
- risks collision and instability across reload or reordering.

## Recommendation

Select **Option A**. It introduces canonical identity through the established
manager boundary, preserves compatibility explicitly, and keeps legacy data
truthful rather than inventing correlations.

## Required Separate Work

- bounded Objective/ObjectiveManager/ObjectiveRegistry implementation;
- duplicate-ID error contract;
- downstream Plan and QueueItem propagation;
- write-forward or migration policy;
- recovery API and re-execution behavior.
