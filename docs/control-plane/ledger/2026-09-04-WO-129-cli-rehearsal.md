# WO-129 — Fresh-Process CLI Rehearsal

2026-09-04, baseline 8f977e4, feat/operational-builder-chain.
Authority: owner requested next step from HANDOFF-108; OWNER-DECISION-026.
Scope: reproducible ledger probe and records only. Exercise public build,
standalone CLI use, persisted discovery, collision and disabled recovery using
disposable state/output. Preserve successful records/output and verify coherent
failure, read-only denials, cleanup and unchanged active data. Reuse WO-121 helpers.
No product source, credentials, provider, architecture or permission changes.
Verify probe, syntax and regression suite; stop after recording and checkpoint.
Rollback is removal of this probe/records if requested; no data migration.

Complete: eight-process rehearsal and probe compile pass. See VERIFICATION-109
and HANDOFF-109. Stop; no new capability is authorized by this record.
