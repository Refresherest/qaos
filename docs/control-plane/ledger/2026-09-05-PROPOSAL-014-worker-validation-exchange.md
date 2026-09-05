# PROPOSAL-014 — Immutable Worker Validation Exchange

Status: ACCEPTED by OWNER-DECISION-035. Detailed contract and evidence are in
WO-169. Acceptance establishes the staged direction; it is not direct authority for
credential creation, worker mutation, transfer or generated-code execution.

## Recommendation

Select a controller-initiated, one-request/one-response framed exchange over the
existing SSH listener using a new dedicated restricted key and forced broker command.
Expose no new port. Accept no archive, caller command, image, runtime option, path
destination, environment or host mount. Bind request/result to canonical Objective,
Task and immutable Artifact IDs/digests; persist validated evidence in QueueItem.result.

Before generated candidates are admitted, add immutable Artifact identity,
content digest and bounded provenance through a separate backward-compatible schema
work order. The current title-only overwrite behavior is not sufficient evidence of
immutable bytes.

## Staging

1. Owner selects the artifact and transport options in DECISION-REQUEST-021.
2. Implement and independently verify Artifact identity/digest/provenance locally.
3. Separately create the restricted worker identity, forced broker and exact sudoers
   boundary; never reuse the admin or OmniRoute keys.
4. Verify only synthetic framed exchanges, replay/schema/path/hash failures and exact
   cleanup.
5. Return for a new decision before any generated candidate or QAOS source transfer.

No implementation, credential creation, worker mutation or execution is authorized
by this proposal.
