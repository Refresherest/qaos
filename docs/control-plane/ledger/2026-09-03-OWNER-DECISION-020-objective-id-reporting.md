# OWNER-DECISION-020 — Objective ID Reporting

## Decision

The owner selected Option A from DECISION-REQUEST-020, adopting PROPOSAL-013.

## Governing Contract

- OperationalSession exposes create_objective(goal) using existing validation
  and persistence, and execute_objective(objective) accepting only the exact
  canonical Objective registered in that session's workspace.
- Execution uses the existing Kernel path and pending-failure lifecycle guard.
  execute_goal remains a compatible composition with unchanged result and
  original internal exception behavior.
- The CLI creates once, prints the exact Objective ID to stdout before execution,
  and executes that same object. No latest-record or goal-based inference.
- Preserve final success summary fields and exit codes. Failure remains exit 1
  with exception-type-only stderr diagnostics rather than raw exception payloads.
- Preserve existing identity validation and test invalid generated IDs. Do not
  truncate identity, create a failure aggregate, mutate arbitrary exceptions,
  or wrap the original exception.

## Scope

Authorize a separate bounded work order for OperationalSession, objective CLI
adapter/main wiring, application/CLI/subprocess tests and records. Verify single
creation, same-session membership, original exception identity, safe CLI errors
and use of the reported ID for recovery. No listing changes, recovery internals,
automatic retry, UI, migration, providers, credentials or durable audit policy.
