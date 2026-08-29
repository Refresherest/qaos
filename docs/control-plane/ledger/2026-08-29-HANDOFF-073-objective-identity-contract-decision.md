# HANDOFF-073 — Objective Identity Contract Decision

## Branch and Baseline

- Branch: `feat/operational-builder-chain`
- Input baseline: `74cfe27`
- Work order: WO-082

## Completed

OWNER-DECISION-013 records the owner's selection of Option A from
DECISION-REQUEST-013. The governing contract uses manager-injected opaque IDs,
canonical ID plus latest-by-goal registry indexes, complete-record persistence,
and pass-through loading for unidentified legacy records.

## Verified Boundary

This checkpoint changes control-plane documentation only. No QAOS product code,
tests, schemas, active runtime data, OpenHands profiles, provider settings, or
credentials changed. Unrelated working-tree changes remain excluded.

## Open Finding

FINDING-036 remains open. Selecting the identity contract does not implement
identity propagation or authorize ordinary queue processing as recovery.

## Next Work Package

Implement only the Objective, ObjectiveManager, and ObjectiveRegistry identity
foundation governed by OWNER-DECISION-013, including deterministic generator
injection, dual indexes, complete-record persistence, legacy pass-through, and
fail-closed duplicate-ID handling. Do not propagate identity to Plan or
QueueItem, migrate legacy data, or implement recovery in that work package.
