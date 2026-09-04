# WO-125 — Fresh-Process Trusted Template Rehearsal

Baseline 591ea3b on feat/operational-builder-chain, 2026-09-04.
Authority: owner requested next step from HANDOFF-104; OWNER-DECISION-025.
Objective: demonstrate the existing template contract across fresh processes.
Scope: one reproducible ledger probe, verification/handoff and current-state
records. Reuse public OperationalSession, persisted discovery and WO-121 probe
helpers. No product source, providers, credentials, CLI or new template changes.

Requirements: disposable state/output; build text_stats_v1; import and use its
function in another process without output or file mutation; discover persisted
completion; cause a same-target collision; deny recovery without template opt-in
without writes; retain coherent failure and original successful records/output.
Verify bounded subprocess results, active-data hashes/timestamps, cleanup,
regression tests and syntax/architecture inspection. Preserve unrelated dirt.
Stop after recording results; a defect requires reporting, not scope expansion.

Completed: six-process probe passed; 245 regression tests passed; probe compile
and architecture inspection completed. See VERIFICATION-107 and HANDOFF-105.
Rollback: remove only this work order's probe/records if requested; no product
or active-state migration exists. Probe cleans only its own temporary directory.
