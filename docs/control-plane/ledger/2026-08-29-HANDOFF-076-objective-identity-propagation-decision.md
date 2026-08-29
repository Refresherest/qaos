# HANDOFF-076 — Objective Identity Propagation Decision

## Branch and Baseline

- Branch: `feat/operational-builder-chain`
- Input baseline: `2ae0d77`
- Work order: WO-085

## Completed

OWNER-DECISION-014 records the owner's selection of Option A from
DECISION-REQUEST-014. Plan and QueueItem will carry additive, non-owning
Objective-ID references while retaining goal text and truthful legacy omission.
PlanRegistry will use canonical ID and latest-by-goal indexes plus complete
records; QueueItems may share one Objective reference.

## Verified Boundary

This checkpoint changes control-plane documentation only. Product code, tests,
schemas, active data, migration, recovery, filtering, continuation, guards,
credentials, providers, OpenHands profiles, and unrelated files are unchanged.

## Open Finding

FINDING-036 remains open. The selected propagation contract does not implement
the references or authorize recovery.

## Next Work Package

Implement only OWNER-DECISION-014 across Plan, PlanRegistry, PlannerManager,
QueueItem, QueueManager, CouncilManager, and ExecutionEngine with focused and
regression verification. Do not migrate legacy records or add recovery,
filtering, continuation, or queue guards.
