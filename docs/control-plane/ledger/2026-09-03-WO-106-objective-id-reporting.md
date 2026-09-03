# WO-106 — Objective ID Reporting

Implement OWNER-DECISION-020 at baseline 9702ba9. Scope: OperationalSession,
objective adapter/main, focused tests and records. Expose creation and exact
same-session canonical execution; preserve execute_goal and original internal
exceptions. Print CLI ID before execution and use safe failure diagnostics.

No recovery/listing changes, migration, providers, credentials, UI or unrelated
edits. Verify single creation, membership rejection, success/failure output,
reported-ID recovery, regression, compile/import/architecture and scope checks.
Record, commit, push, then stop.
