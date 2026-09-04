# WO-128 — Implement Trusted CLI Template

2026-09-04; baseline 5cbe017 on feat/operational-builder-chain.
Authority: OWNER-DECISION-026 and owner request to proceed.
Objective: implement text_stats_cli_v1 exactly within WO-126's approved contract.
Scope: trusted source/fixtures, template-ID selection, narrow lifecycle verifier
hook, focused tests and control-plane records. Reuse existing Task/Plan/Queue
and authorization; preserve old template bytes, print-only contract and defaults.
No arbitrary code/commands, providers, credentials, QAOS CLI, multi-file, UI or
Content OS expansion. Preserve all unrelated working-tree changes.

Verify fixed CLI inputs/counts/exit streams including limits and invalid forms,
standalone fresh-process use, import silence, corrupted CLI rejection despite
self-test success, permissions/reload, confinement/collision and failure states.
Run focused/full regressions, compile/import/architecture and active-data checks.
Stop after verification and records. No automatic next work order. Rollback, if
requested, reverts only this scoped change, with no active-data migration.

Complete: 30 focused tests and 253 full regression tests pass; compile and 192
module imports pass. Active data unchanged. See VERIFICATION-108/HANDOFF-108.
