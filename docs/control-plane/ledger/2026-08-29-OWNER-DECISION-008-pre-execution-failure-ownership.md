# OWNER-DECISION-008 — Pre-Execution Failure Ownership

## Status

`ACCEPTED`

## Decision

The owner selected **Option A — OperationalSession Owns Pending Failure** from
DECISION-REQUEST-008.

When Kernel invocation raises and the application-created Objective remains
`pending`, OperationalSession must fail it through its shared ObjectiveManager
and re-raise the original exception. If downstream work already changed the
Objective state, OperationalSession must not overwrite or repeat that
transition.

ExecutionManager retains its established `start -> complete/fail` authority.
This decision does not change post-execution failure, retry, recovery, or
persisted-error policy.
