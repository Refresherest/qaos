# WO-104 — Objective ID Reporting Assessment

## Objective and Context

Assess canonical Objective-ID output for normal CLI execution, especially when
execution fails. Baseline c2e6b69 on feat/operational-builder-chain.

## Evidence and Scope

commands/objective.py receives only the result after execute_goal succeeds.
execute_goal creates the Objective internally and rethrows the original error,
so failure leaves the caller without that Objective. Compare contracts that do
not guess identity or replace the original exception. Documentation only.

## Non-Goals and Stop

No source, tests, output changes, exception wrapping, data repair, recovery,
providers, credentials, UI, migration or unrelated edits. Record options,
validate and push, then stop for owner selection.
