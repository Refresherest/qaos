# HANDOFF-056 — One-Shot CLI Objective Adapter

## Work Order

`WO-065`

## Status

`COMPLETE — ACCEPTED`

## Result

OWNER-DECISION-006 is implemented. QAOS now has a direct manual execution path:

`python -m qaos.main objective --workspace <path> <goal...>`

The command requires explicit workspace selection and delegates through
OperationalSession. It never defaults to the repository's active data.

## Verification

- Focused tests: 21 passed
- Full suite: 103 passed
- Import sweep: 184 modules
- Compile: passed
- Architecture inspection: 186 Python files; unrelated findings unchanged
- Active data: unchanged
- Reviewer: ACCEPT

## Intentionally Untouched

- Kernel, Runtime, Executive, OperationalSession, and legacy command behavior
- Content OS, providers, models, credentials, fallback, retry, and deployment
- All unrelated modified and untracked working-tree files

## Next Executable Step

Run one owner-approved manual CLI smoke test against a fresh disposable
workspace, or record a separate decision before any additional adapter or
Content OS integration.

## Stop Condition

WO-065 is complete. Stop before running a non-test manual objective or adding
another interface.
