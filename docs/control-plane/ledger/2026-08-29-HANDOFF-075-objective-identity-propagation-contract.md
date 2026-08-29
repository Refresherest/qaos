# HANDOFF-075 — Objective Identity Propagation Contract

## Branch and Baseline

- Branch: `feat/operational-builder-chain`
- Input baseline: `ecc32b2`
- Work order: WO-084

## Completed

The bounded Plan and QueueItem propagation assessment is complete.
PROPOSAL-007 recommends additive non-owning Objective ID references, dual Plan
indexes with complete-record persistence, and QueueItem pass-through that
permits multiple items to share one Objective reference.

## Proven Facts

- PlanRegistry and ExecutionEngine are currently goal-keyed.
- Equal-goal Plans can collapse or be selected for the wrong invocation.
- Current QueueItem construction and persistence discard Objective identity.
- Legacy active records contain no Objective identity reference.

## Preserved Boundaries

No product code, tests, schemas, active data, migration, recovery, queue
processing, providers, models, credentials, OpenHands profiles, or unrelated
working-tree files changed.

## Decision Required

Select Option A, B, or C in DECISION-REQUEST-014. Option A is recommended.

Implementation remains unauthorized until the owner selects a contract.
