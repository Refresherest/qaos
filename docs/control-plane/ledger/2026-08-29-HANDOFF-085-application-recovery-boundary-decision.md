# HANDOFF-085 — Application Recovery Boundary Decision

## Branch and Baseline

- Branch: `feat/operational-builder-chain`
- Input baseline: `4e2b97c`
- Work order: WO-094

## Completed

OWNER-DECISION-017 records the owner's selection of Option A. The approved
application boundary is a canonical-ID-only OperationalSession recovery method
that delegates through ExecutiveManager directly to the existing
ExecutionManager and returns the canonical completed Objective.

## Verified Boundary

This checkpoint changes control-plane documentation only. Product code, tests,
APIs, schemas, active data, internal recovery, Kernel, CLI, UI, retry policy,
migration, credentials, providers, and unrelated files remain unchanged.

## Next Work Package

Implement only OWNER-DECISION-017 across ExecutiveManager, create_executive,
OperationalSession, focused tests, and control-plane records. Prove normal
pipeline stages are bypassed and preserve every explicit exclusion.
