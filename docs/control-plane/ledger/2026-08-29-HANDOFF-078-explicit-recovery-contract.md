# HANDOFF-078 — Explicit Recovery Contract

## Branch and Baseline

- Branch: `feat/operational-builder-chain`
- Input baseline: `0e2dbb8`
- Work order: WO-087

## Completed

The bounded recovery assessment is complete. PROPOSAL-008 recommends explicit
Objective-ID recovery that retries the single failed item and then its pending
remainder, preserves completed work, and leaves unrelated attempts untouched.

Ordinary processing would skip pending items only when their identified attempt
already contains a failed item. This prevents implicit continuation without a
global queue block.

## Preserved Boundaries

No product code, tests, APIs, schemas, active data, migration, legacy
association, recovery, queue-policy change, provider, model, credential,
OpenHands profile, or unrelated working-tree file changed.

## Decision Required

Select Option A, B, or C in DECISION-REQUEST-015. Option A is recommended.

Implementation remains unauthorized until the owner selects a contract.
