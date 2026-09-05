# DECISION-REQUEST-021 — Worker Validation Exchange

## Status

`RESOLVED — OWNER-DECISION-035`

On 2026-09-05 the repository owner replied "approve" and selected Artifact option
A1, transport option A and the recommended three-stage sequence. The authority
boundary below remains in force; implementation proceeds only through separately
scoped work orders.

## Decision 1 — Artifact identity prerequisite

- **A1 (recommended):** add backward-compatible immutable Artifact ID,
  content digest and bounded provenance before candidate transport.
- **A2:** retain title plus transient manifest digest; smaller but cannot guarantee
  retained canonical bytes after title replacement.
- **A3:** place candidate bytes in QueueItem.result; rejected because it inverts
  Artifact ownership.

## Decision 2 — Authenticated transport

- **A (recommended):** dedicated restricted SSH identity plus forced, length-framed
  broker over existing port 22; no archive, shell, SFTP or new listener.
- **B:** reuse admin SSH/SFTP manually; broad authority and mutable steps make it
  unsuitable for generated-job admission.
- **C:** HTTPS/mTLS service; adds listener and certificate/service lifecycle.
- **D:** cloud object/queue polling; adds credentials, egress, cost and provider coupling.

## Decision 3 — Sequencing

Recommended sequence:

1. Artifact identity/digest/provenance decision and local implementation/review.
2. Separate restricted-key/broker implementation and synthetic exchange review.
3. New owner decision before any generated-code or QAOS-source transfer.

## Requested owner response

Approve, revise or reject each:

1. Artifact option A1.
2. Transport option A.
3. The three-stage sequencing and continued generated-code prohibition.

Approval authorizes only a separate record of the decisions. It does not authorize
code changes, key creation, worker mutation, transfers or generated-code execution.
