# OWNER-DECISION-037 — Durable Pilot Attempt Authority

2026-10-04. Authority: the repository owner replied, "I approve 1A, 2A,
3A, and 4A" to DECISION-REQUEST-024.

## Accepted architecture

1. New QueueItems gain an opaque immutable queue record ID. A single
   canonical QueueItem owns its frozen pilot-attempt envelope; Objective and
   Task IDs remain correlations, not QueueItem identity. Legacy items are not
   silently backfilled or pilot-eligible.
2. An explicitly selected, local-filesystem SQLite queue is the transactional
   authority for this implementation. All queue writes and dispatch selection
   in that workspace must use a fresh transaction or refuse. Existing JSON
   remains the default; no dual authority or active migration is approved.
3. The exact request and Artifact claim must commit before any possible
   outbound byte. Ambiguity leaves `pilot_claimed` or `pilot_unknown` held;
   neither may be retried, rebuilt, or admitted through ordinary recovery.
   Artifact identity/provenance/bytes are rechecked before a send. A later
   offline frame is not authenticated by matching fields or an unkeyed hash.
4. Pilot QueueItem states remain distinct from Task/Objective lifecycle.
   Pending siblings of the same Objective are held; unrelated generic queue
   work may proceed. Generic recovery refuses the whole attempted-pilot
   Objective. Evidence/adjudication never follows from a mere worker outcome.

## Release boundary

This decision authorizes WO-178 as a **local-only** implementation and
verification. It does not authorize active-data migration, a live sender,
worker/cloud mutation, credentials, candidate transfer, generated-code
execution, late-status admission, Task/Objective adjudication, model
designation or spending. A real authenticated response writer and any active
cutover each require a later scoped approval.
