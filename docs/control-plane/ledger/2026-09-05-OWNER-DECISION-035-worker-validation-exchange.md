# OWNER-DECISION-035 — Worker Validation Exchange

2026-09-05. Authority: the repository owner replied "approve" to
DECISION-REQUEST-021 and approved all three recommended selections.

## Decisions

1. Select Artifact option A1: add backward-compatible immutable opaque Artifact
   identity, a byte-oriented content SHA-256 digest and bounded provenance. Preserve
   title lookup for compatibility, reject duplicate immutable IDs and preserve
   legacy missing-ID loads without silently writing forward. Exact content
   canonicalization remains an implementation-contract question that must be made
   explicit and verified in the separate Artifact work order.
2. Select transport option A: use a dedicated restricted SSH identity and a forced,
   length-framed broker over the existing port 22. Do not reuse the administrative
   or OmniRoute keys, expose a new listener, accept archives, or grant shell/SFTP
   authority.
3. Select the staged sequence: implement and independently verify Artifact A1
   locally; separately implement and verify the restricted transport with synthetic
   exchanges; then return for a new owner decision before transferring or executing
   generated code or QAOS source.

## Authority boundary

This decision resolves the architecture choices and authorizes preparation and
execution of a separately scoped Artifact A1 work order as the next step. It does
not itself authorize product-code changes, credential or key creation, worker user,
SSH or sudoers changes, broker implementation, network changes, candidate or QAOS
source transfer, generated-code execution, cloud changes, model validation or model
designation.

The restricted transport is approved as the later design direction, not as current
mutation authority. Work must stop after the Artifact work order is implemented and
independently verified, before transport setup begins without separate authorization.
