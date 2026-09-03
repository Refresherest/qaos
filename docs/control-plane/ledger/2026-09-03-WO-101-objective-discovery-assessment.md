# WO-101 — Objective Discovery Assessment

## Objective and Context

Assess read-only operator discovery of Objective IDs needed by the recovery
CLI. Baseline 4f3cd0c on feat/operational-builder-chain.

## Scope

Inspect ObjectiveManager, ObjectiveRegistry, Stores, JSONStore and CLI contracts.
Define listing, legacy handling, output, read-only guarantees and owner options.

## Non-Goals

No implementation, runtime-data mutation, recovery changes, UI, migration,
provider/credential changes, automatic retry or unrelated edits.

## Verification and Stop

Use complete record enumeration, preserve missing identities, distinguish status
from recovery eligibility, validate record consistency and staged scope. Record,
commit, push, and stop for owner selection.
