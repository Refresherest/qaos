# DECISION-REQUEST-011 — Later-Call Continuation

## Decision Required

Choose whether an ordinary QueueManager processing call may continue pending
work left by an earlier failed call.

## Evidence

WO-077 proves that a second call silently changes the prior fail-fast state
from `completed, failed, pending` to `completed, failed, completed`. The queue
has no attempt or batch identity with which to distinguish recovery work from
unrelated pending work.

## Options

### Option A — Explicit Recovery Boundary with Attempt Identity (Recommended)

Do not designate ordinary `process()` as recovery. Introduce a separately
scoped attempt/batch identity and explicit recovery operation before allowing a
failed plan's pending remainder to continue. Preserve current runtime behavior
temporarily as unapproved compatibility behavior until that larger work is
implemented; do not expose or invoke it as recovery.

Consequences:

- prevents accidental recovery semantics from becoming architecture;
- enables future recovery to target one failed attempt safely;
- requires a separate design and schema work order before enforcement;
- avoids blocking unrelated pending work with a naive global failure guard.

### Option B — Designate Ordinary Processing as Continuation

Make repeat `process()` calls the official mechanism for completing all
remaining pending queue work, even when failed items coexist.

Consequences:

- matches current behavior and needs little implementation;
- continues work without confirming dependencies or failed-Objective state;
- conflates routine queue draining with recovery.

### Option C — Freeze Any Queue Containing Failure

Reject ordinary processing whenever failed and pending items coexist.

Consequences:

- prevents implicit continuation immediately;
- can block unrelated pending objectives because queue entries lack attempt
  identity;
- creates a global operational deadlock until separate cleanup is performed.

## Recommendation

Select **Option A**. It preserves the architectural distinction between routine
execution and recovery without introducing a global guard that cannot identify
which pending work belongs to the failed attempt.

## Explicitly Separate Future Decisions

- attempt/batch identity schema and migration;
- recovery API authorization and caller;
- dependency and prerequisite semantics;
- retry of failed work versus continuation of unattempted work;
- provider/model fallback and deployment policy.
