# WO-142 — Builder CLI Operator Walkthrough

2026-09-04; baseline d2efdcc; feat/operational-builder-chain.
Authority: owner proceed on HANDOFF-121. Objective: a reproducible operator
example of the shipped CLI, including successful use and safe failure diagnostics.
Scope: ledger probe, operator instructions/results, handoff and current-state
records only. Reuse existing fingerprint helpers. No product/test edits, models,
providers, credentials, new permission, recovery behavior or active-data migration.
Use uniquely owned disposable roots. Verify build/use/tests/discovery, missing
permission, missing/overlapping roots, collision and unprivileged recovery;
assert early refusals do not write, successful records/output persist and active
data stays unchanged. Run focused CLI regressions and probe compile/record checks.
Stop after verified documentation checkpoint. Preserve unrelated work.

Complete: nine walkthrough phases and 82 focused CLI tests pass; active data
unchanged in the probe. See VERIFICATION-116 and HANDOFF-122. Rollback/revision
is limited to these records/probe, never product data or existing output.
