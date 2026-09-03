# PROPOSAL-013 — Report Objective ID Before Execution

## Recommended Contract

- Add OperationalSession.create_objective(goal) and execute_objective(objective).
  create_objective applies execute_goal's existing string/blank validation and
  persists one canonical identified Objective. execute_objective accepts only
  the exact canonical Objective registered in that session's workspace, then
  uses the existing Kernel path and pending-failure lifecycle guard.
- Preserve execute_goal as a compatibility composition of those methods with
  unchanged success result and original exception behavior.
- The objective CLI creates first, prints `Objective ID: <exact id>`, then
  executes that same object. The ID is therefore visible on both success and
  failure without looking up the latest record or guessing from a goal.
- Keep existing final success summary fields and exit codes. On failure, retain
  exit 1 but adopt recovery CLI's safe diagnostic style: exception type only,
  not raw exception payload. ID output is stdout before worker output; failure
  diagnostic remains stderr.
- Escape/control-safe representation is unnecessary for generated opaque IDs,
  but tests must reject a malicious custom ID generator before CLI use if it
  violates existing nonempty-string validation. Do not truncate the ID.
- Do not create a new result/failure aggregate, attach metadata to arbitrary
  exceptions, wrap the original exception, or infer identity after failure.

## Architectural Consequence

ObjectiveManager remains identity source and lifecycle persistence owner;
OperationalSession remains workspace application owner; Kernel still executes
a canonical Objective. The two new methods expose existing steps rather than a
duplicate Objective concept. Session membership validation is essential to
prevent cross-workspace execution.

## Implementation Boundary

If selected, change OperationalSession, objective adapter/main wiring, focused
application/CLI/subprocess tests and records. Verify compatibility, exact single
creation, cross-workspace rejection, original exception identity internally,
safe CLI errors and failure ID usefulness with the recovery command.

No listing changes, recovery internals, automatic retry, UI, migration, provider
changes, credentials, or durable audit policy.
