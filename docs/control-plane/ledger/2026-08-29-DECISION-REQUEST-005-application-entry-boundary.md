# DECISION-REQUEST-005 — Application Entry Boundary

## Status

`OWNER DECISION REQUIRED`

## Evidence

WO-061 provides `create_executive(stores, objectives=..., logger=...)`, but an
application caller must still construct Stores, a shared ObjectiveManager,
Configuration, and Kernel before it can create and execute a canonical
Objective.

The current CLI is a legacy command dispatcher. It has no objective command,
workspace-selection contract, or raw-goal contract. Kernel intentionally
rejects raw strings. Content OS has a separate verified
`BriefToReviewedDraft` workflow and should not be coupled to the generic
Executive merely to provide its first consumer.

## Decision

Choose the first application-facing execution boundary.

### Option A — Operational Application Session (Recommended)

Add a provider-neutral application-layer session/facade that owns one Stores
workspace, one ObjectiveManager, the composed Executive, and one Kernel. Its
public operation accepts a goal, creates the canonical Objective through the
shared manager, and returns the existing ExecutionResult.

Consequences:

- gives programmatic callers one coherent lifecycle boundary;
- preserves Kernel's canonical-Objective contract;
- provides a reusable base for a later CLI or other interface;
- introduces a deliberately broader application API whose exact name,
  validation, and override parameters must be scoped in implementation.

### Option B — CLI Objective Command First

Add a CLI command that accepts a goal and directly constructs the operational
graph.

Consequences:

- gives the owner a visible manual execution path immediately;
- forces CLI workspace, output, exit-code, and input policy choices now;
- risks embedding composition policy in a presentation adapter before a
  reusable application boundary exists.

### Option C — Keep Explicit Caller Composition

Do not add another boundary. Require every application to construct Stores,
ObjectiveManager, Executive, Configuration, and Kernel explicitly.

Consequences:

- adds no public API;
- preserves maximum caller control;
- duplicates lifecycle-sensitive wiring and increases the chance that
  objective creation and persistence use different managers.

## Recommendation

Select **Option A**. It creates one reusable application boundary above the
verified Executive factory without weakening Kernel or prematurely coupling
QAOS to its CLI. A later CLI can become a thin adapter over that boundary.

## Explicitly Deferred

- exact facade name and optional dependency overrides;
- CLI command syntax, output, and exit codes;
- Content OS integration;
- provider/model selection;
- fallback, retry, deployment, and remote execution policy.
