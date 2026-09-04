# WO-141 — Explicit Builder CLI

2026-09-04; baseline 5d13fc3; feat/operational-builder-chain.
Authority OWNER-DECISION-029; all WO-139 acceptance requirements apply.
Implement only a thin build-project command, help/routing and focused tests.
Reuse typed intent, existing application lifecycle and filesystem safeguards.
No API permission changes, recovery flags, new rendering, providers or active-data
migration. Verify parser/no-write refusals, seven selections, root boundaries,
fresh-process build/use/discovery/collision, sanitized errors and full regressions,
compile/import/architecture checks. Preserve unrelated work; record and stop.

Complete: 354 tests, compile and 196 imports pass; active data unchanged.
See VERIFICATION-115 and HANDOFF-121. Stop before operator walkthrough.
Rollback if requested is limited to the scoped adapter/help/tests/records;
no migration, adoption or deletion of previously published output.
