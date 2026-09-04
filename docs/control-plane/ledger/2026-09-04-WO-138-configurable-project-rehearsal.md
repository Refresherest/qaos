# WO-138 — Configurable Project Rehearsal

2026-09-04; baseline 5111dd6; feat/operational-builder-chain.
Authority: owner proceed on HANDOFF-117; OWNER-DECISION-028 contracts unchanged.
Objective: reproduce v2 normalization, saved metrics, standalone use, discovery,
permission/collision refusal and successful-record preservation in fresh processes.
Scope: ledger probe and records, CURRENT_STATE.md and PROJECT_STATE.json.
Reuse WO-134 rehearsal and WO-121 fingerprint helpers; no new product abstraction.
Disposable repository-confined state/output only. No product changes, credentials,
providers, OpenHands, active-data migration, output adoption or feature expansion.
Verify nine top-level fresh processes, exact four files/digests, normalized saved
metrics and selected output, default/v1-only/root-only refusal without writes,
authorized collision recovery refusal, coherent failed state and preserved success.
Run full regression suite, probe compile, JSON and whitespace checks.
Preserve unrelated working-tree changes. Stop after results, checkpoint and handoff.

Complete: nine-process rehearsal and 307 regressions pass; active data unchanged.
See VERIFICATION-114 and HANDOFF-118. Rollback, if requested, is limited to this
probe and these records; no product/state migration or published-output deletion.
