# OWNER-DECISION-036 — First Real Worker Admission

2026-09-06. Authority: the repository owner replied
"approve all three A options" to DECISION-REQUEST-022.

## Decisions

1. The first candidate scope is one dependency-free generated Python pilot
   Artifact containing one UTF-8 file, paired with one separately authored
   acceptance Artifact. No QAOS source or third-party dependencies.
2. Canonical Artifact IDs/digests own candidate and acceptance bytes;
   Objective/Task IDs correlate the request; the originating QueueItem.result owns
   the validated bounded response projection.
3. Permit one manual attempt only, without automatic retry, network, dependency
   download, publication, Artifact promotion or model VALIDATED/DESIGNATED change.

## Authority boundary

This decision authorizes a separately scoped local-only implementation and
independent test work order for the pilot admission package, fixed launcher fixture
and QueueItem result projection. It does not authorize model calls, live worker
mutation, candidate or QAOS-source transfer, real generated-code execution,
publication, promotion or spending.
