# DECISION-REQUEST-023 — Local Bridge Toward One Live Python Pilot

Status: OPEN — owner selection required. Basis: WO-175 after WO-174 local-only
verification. This request does not authorize worker mutation or code execution.

## Decision 1 — Pilot enablement and rollback

- **A (recommended):** implement an opt-in, pinned pilot broker entrypoint and
  incremental installer/rollback, preserving the existing synthetic route,
  restricted identity, sudoers and administrative SSH. Keep the pilot disabled
  by default. Test and independently review locally before any installation.
- **B:** replace or reuse the existing whole-transport installer/rollback for
  the pilot. Reject: failure could remove a working, separately verified path.

## Decision 2 — Attempt authority before dispatch

- **A (recommended):** keep the local deployment bridge separate from dispatch.
  Before any real one-shot transport implementation, commission a CSA contract
  for a durable pre-dispatch claim and `UNKNOWN` recovery under canonical
  QueueItem authority, including cross-process exclusivity and request/Artifact
  correlation. Reconcile existing queue lifecycle/storage and preserve
  `QueueItem.result` as validated response evidence unless a later owner
  decision explicitly changes it. Independently test before live use.
- **B:** rely on an in-memory "one shot" flag, broker replay keyed by a fresh
  request ID, or an automatic retry after SSH loss. Reject: the first request
  may already have executed, and the present queue save has no atomic claim.

## Decision 3 — Release gate and spending

- **A (recommended):** stop after local bridge tests and independent review.
  Before any live attempt, obtain a separately approved attempt-authority
  implementation, fresh account/worker/network/cleanup evidence,
  exact candidate and acceptance identities and origin, an explicit spending
  ceiling, and a separate owner approval for the targeted live change and one
  request. Do not downgrade `runsc`, pull an image, open ingress, create a new
  resource or upgrade the account as an incidental step.
- **B:** deploy and run immediately based on the local suite and historical
  free-tier screenshots. Reject: those do not establish present security or
  account-specific charge state.

## Requested owner response

Approve, revise or reject Decisions 1A, 2A and 3A. Approval scopes the next
work order to **local deployment-bridge implementation and verification only**.
It does not authorize a model call, candidate generation, credential access,
live pilot installation, transfer, dispatch, Docker execution, OCI change,
production QueueItem write or spend. A separate CSA decision and later
implementation are required for durable attempt ownership. Live actions need
the later evidence and explicit approval described in WO-175. If a different
live payload or cost tolerance is desired, state it at that later gate.
