# HANDOFF-086 — Application Recovery

## Baseline and Work

- Branch: feat/operational-builder-chain
- Input commit: a2866e7
- Work order: WO-095; authority: OWNER-DECISION-017

## Completed

OperationalSession.recover_objective selects an existing canonical Objective ID
in its explicit workspace and returns the canonical Objective after recovery.
ExecutiveManager delegates directly to the factory's shared ExecutionManager.
Kernel, CLI, and the normal Executive pipeline are unchanged.

Modified source: application/session.py, executive/manager.py,
executive/factory.py. Added tests/test_application_recovery.py and WO-095,
VERIFICATION-088, this handoff; updated CURRENT_STATE and PROJECT_STATE.

## Verification

152 tests passed, including 8 new cases; compile and 184-module import sweeps
passed. Architecture inspection retained only existing unrelated findings.
Scope excludes internal recovery changes, migration, providers, credentials,
automatic retry, audit evidence, and unrelated files.

## Next Work Package

Perform one bounded recovery rehearsal using a disposable workspace and the
programmatic OperationalSession boundary. Do not add CLI/UI or retry policy.
