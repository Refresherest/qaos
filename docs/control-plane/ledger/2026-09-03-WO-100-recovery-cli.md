# WO-100 — One-Shot Recovery CLI

## Objective and Context

Implement OWNER-DECISION-018 over OperationalSession without changing recovery
ownership. Baseline: 31de5be, feat/operational-builder-chain.

## Scope

main.py, commands/recover.py, focused CLI/subprocess tests, and ledger records.
Require exact syntax, existing workspace, unchanged ID, one delegation, canonical
completed status, human-readable summary and exit statuses 0/1/2.

## Non-Goals

Kernel, existing commands, recovery internals, ID discovery, UI, historical data,
automatic retry, providers, credentials, and unrelated edits remain unchanged.

## Verification and Stop

Verify invalid usage, missing workspace, status handling, safe errors, exact ID,
and actual failed execution followed by CLI recovery in a disposable workspace.
Run regression, compile/import/architecture and data/scope checks. Record,
commit, push, and stop.
