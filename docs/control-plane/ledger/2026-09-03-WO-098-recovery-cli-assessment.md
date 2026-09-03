# WO-098 — Recovery CLI Assessment

## Objective and Context

Assess operator access to verified OperationalSession recovery. Input baseline:
0a52f1f, feat/operational-builder-chain. The existing objective CLI delegates to
an explicit-workspace session and uses exit statuses 0/1/2.

## Scope

Inspect main.py, commands/objective.py and the current recovery contracts;
define syntax, workspace/ID validation, output, errors, and exclusions. Record
options and request owner selection.

## Non-Goals

No product code, tests, API implementation, data mutation, credentials, providers,
UI, migration, automatic retry, or unrelated changes.

## Verification and Stop

Check proposal against existing CLI and application ownership; validate records
and staged scope. Commit and push the assessment, then stop for owner selection.
