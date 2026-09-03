# HANDOFF-097 — Objective ID Reporting

Baseline 9702ba9, feat/operational-builder-chain. WO-106 implements
OWNER-DECISION-020.

OperationalSession now exposes create_objective and exact same-session
execute_objective; execute_goal composes them. The objective CLI prints and
flushes ID before execution and uses safe failure diagnostics.

Modified session.py, commands/objective.py, main.py and the approved failure
output assertion in test_cli_kernel.py. Added test_objective_id_reporting.py,
WO-106, VERIFICATION-099 and this handoff; updated state records.
182 tests pass; compile/import checks pass; active data and unrelated work remain
unchanged.

Next bounded step: rehearse the complete operator flow (create/fail, discover,
recover, rediscover) in a disposable workspace, recording evidence without new
features or architecture decisions.
