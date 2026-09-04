# WO-137 — Configurable Project v2

2026-09-04; baseline 8858230; feat/operational-builder-chain.
Authority OWNER-DECISION-028. Implement required immutable normalized metric
selection on python_project v2, separately enabled text_stats_project_v2, trusted
four-file rendering and independent selected-key acceptance. Reuse existing
publication/lifecycle; preserve all v1 source bytes/records/behavior.
Scope: typed intent, narrow routing/authority, rendering/verifier, tests/records.
No models, arbitrary code, dependencies, platforms, UI or output editing.
Verify seven configurations, invalid-input no writes, determinism, mutation,
round trips/reload, permissions, corruption, collision/cleanup/publication gaps,
isolation, full regressions and fresh-process build/use/discovery. Check active
data unchanged. Preserve unrelated work. Stop after verified checkpoint.
Rollback only scoped changes if requested; no migration/adoption/deletion of output.

Complete: 307 regression tests, compile and 195 imports pass; active data unchanged.
See VERIFICATION-113 and HANDOFF-117. Stop before the next rehearsal.
