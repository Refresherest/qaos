# HANDOFF-091 — Recovery CLI

Baseline: 31de5be on feat/operational-builder-chain. Work order: WO-100.
Authority: OWNER-DECISION-018.

## Completed

`python -m qaos.main recover --workspace <path> <objective_id>` now delegates
once to OperationalSession in an existing explicitly selected workspace.
Exit codes: 0 completed, 1 operation failure, 2 invalid usage. Success prints
Objective ID, goal, and status; error payloads are not echoed.

Modified main.py; added commands/recover.py and tests/test_recovery_cli.py.
Added WO-100 and VERIFICATION-093; updated current-state records. Kernel,
recovery internals, providers, credentials, active data, and unrelated work
remain unchanged.

## Verification and Next Step

166 tests pass, including actual failure followed by subprocess CLI recovery.
Compile/import checks pass (185 modules); architecture retains existing findings.

Next bounded assessment: read-only Objective ID/status discovery for operators.
Do not implement discovery or broaden the CLI without a separate owner decision.
