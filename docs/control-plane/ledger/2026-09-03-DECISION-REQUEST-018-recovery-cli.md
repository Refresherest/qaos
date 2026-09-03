# DECISION-REQUEST-018 — Operator Recovery Access

## Status

RESOLVED — OWNER-DECISION-018 selected Option A

## Options

### A — One-Shot CLI Recovery (Recommended)

Adopt PROPOSAL-011: explicit existing workspace plus exact Objective ID, one
recovery invocation, human-readable summary, and exit statuses 0/1/2. Provides
terminal access now, but requires an already-known ID and separate later work
for discovery.

### B — Read-Only Objective Inspection First

Defer recovery CLI implementation and first assess a workspace-scoped listing
or inspection surface to obtain IDs and status. Improves discoverability before
mutation tooling but requires a separate read-only output/selection contract.

### C — Keep Recovery Programmatic

Retain OperationalSession as the sole application-facing boundary. Avoids a new
CLI compatibility contract but requires Python callers for recovery.

## Recommendation and Boundary

Select A for the smallest operator-facing adapter over the proven application
method. This assessment does not authorize implementation. No option implies
UI, automatic retry, migration, provider changes, or audit policy.
