# DECISION-REQUEST-022 — First Real Worker Admission

## Status

`OPEN — OWNER DECISION REQUIRED`

WO-172 verified the restricted worker transport using synthetic bytes only. The
next capability changes the risk class because candidate bytes would become
executable. Select the exact admission boundary below before implementation.

## Decision 1 — First candidate scope

- **A (recommended):** one dependency-free generated Python pilot Artifact, bounded
  to a single UTF-8 file, paired with a separately authored acceptance Artifact. No
  QAOS source or third-party dependencies.
- **B:** a bounded multi-file QAOS patch candidate. Defer because repository context,
  patch application and publication authority are not yet contracted.
- **C:** the whole QAOS repository. Reject for the first admission.

## Decision 2 — Evidence ownership

- **A (recommended):** canonical Artifact IDs/digests identify candidate and
  acceptance bytes; Objective/Task IDs correlate the request; the originating
  QueueItem.result receives only the validated bounded response projection.
- **B:** retain worker results in a new execution registry. Reject because it
  duplicates QueueItem authority.

## Decision 3 — Execution and promotion authority

- **A (recommended):** one manual attempt, no automatic retry, no network, no
  dependency download, no publication, no Artifact promotion and no model
  VALIDATED/DESIGNATED transition. Stop after evidence is recorded.
- **B:** automatically retry, publish or promote on a passing worker result. Reject
  until recovery, publication and governance contracts explicitly authorize it.

## Requested owner response

Approve, revise or reject:

1. candidate scope A;
2. evidence ownership A;
3. execution/promotion boundary A.

Approval authorizes a new local-only work order to implement and independently test
the pilot admission package, fixed launcher fixture and QueueItem result projection.
It does not authorize live candidate transfer, QAOS-source transfer, model calls,
worker mutation or generated-code execution. Those remain behind a separate live
gate after local verification.
