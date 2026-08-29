# DECISION-REQUEST-010 — Partial-Plan Disposition

## Decision Required

Choose the disposition of later pending queue work when an earlier item fails
during one QueueManager processing call.

## Evidence

WO-075 proves that the current sequential call stops at the first failure and
durably records `completed, failed, pending` for both QueueItems and Tasks.
The untouched item is not attempted.

## Options

### Option A — Explicit Fail-Fast Call Boundary (Recommended)

Designate the current call behavior: stop on the first failure, persist exact
state, leave never-attempted later work pending, and propagate the original
exception. Any later continuation requires a separately authorized recovery
operation.

Consequences:

- preserves accurate distinctions between completed, failed, and unattempted;
- avoids executing further work after the Objective has failed;
- requires no new terminal status or error aggregation;
- deliberately defers continuation and retry mechanics.

### Option B — Continue Independent Items and Aggregate Failures

Continue processing later pending items after a failure, then report an
aggregate result.

Consequences:

- maximizes work completed in one call;
- requires new error aggregation and Objective outcome contracts;
- may execute downstream work after an important prerequisite failed.

### Option C — Terminalize Unattempted Remainder

Stop at the first failure and mark every later item and Task with a new
terminal disposition such as blocked or cancelled.

Consequences:

- makes the whole batch terminal;
- requires new canonical statuses and transition rules;
- loses the existing distinction between pending work and policy-blocked work
  unless a new schema is approved.

## Recommendation

Select **Option A**. It formalizes the smallest safe contract already proven by
runtime evidence and postpones continuation/retry design until QAOS has an
explicit recovery boundary.

## Explicitly Separate Future Decisions

- retry and recovery entry points;
- prerequisite and dependency semantics;
- error aggregation and persisted error details;
- blocked/cancelled status vocabulary;
- provider/model fallback and deployment policy.
