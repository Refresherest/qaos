# WO-096 — Recovery Rehearsal

## Objective and Context

Exercise WO-095's application recovery boundary against a failure produced by
the real operational execution path, then reload the workspace before recovery.
OWNER-DECISION-017 governs the application boundary; OWNER-DECISION-015 governs
internal recovery. Input baseline: 1ffce3a, feat/operational-builder-chain.

## Scope

Create a reproducible rehearsal probe and ledger evidence only. Use an isolated
temporary workspace and a process-local controlled Task failure; remove the
failure injection before constructing a fresh OperationalSession for recovery.
Compare persisted Objective, Plan, and Queue state and active-data fingerprints.

## Non-Goals

No product code, active-data repair, credentials, providers, CLI/UI, migration,
retry policy, or unrelated changes. Do not repair discovered defects here.

## Verification and Stop Condition

Run the probe, capture exact outcome and state, verify active data unchanged and
temporary workspace cleanup. Record any blocker and stop after committing and
pushing the scoped evidence; do not claim success when recovery fails.
