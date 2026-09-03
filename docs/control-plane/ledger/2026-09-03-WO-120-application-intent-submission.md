# WO-120 — Application Intent Submission Implementation

Baseline b030801, feat/operational-builder-chain. Authority OWNER-DECISION-024.
Scope: session opt-in/submission, Executive call-specific intent propagation,
factory wiring, PlannerManager one-task planning and focused tests/records.
Preserve ordinary call signatures/behavior, pipeline stages, lifecycle owners,
legacy data, Kernel/CLI and all execution-authority exclusions.

Verify actual public-session source creation and evidence, preflight no-write
rejection, repeat prevention, failure/recovery, isolation, full tests, compile,
imports, architecture inspection and active-data preservation. Stop at verified
completion or a blocking contract inconsistency; do not repair out-of-scope
capability or recovery behavior opportunistically.

Initial verification was BLOCKED by FINDING-039 (7 passed, 1 failed). The owner
explicitly approved extending WO-120 to PythonFileCapability target-rejection
lifecycle handling and its focused tests, then completing verification. Scope
now includes that narrow fix: target checks run inside started Task failure
handling; no output overwrite or new capability authority is permitted.

Completed: public-session intent execution and FINDING-039 resolution verified.
See VERIFICATION-104 and HANDOFF-102. Stop condition reached.
