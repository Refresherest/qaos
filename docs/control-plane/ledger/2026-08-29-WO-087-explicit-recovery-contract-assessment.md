# WO-087 — Explicit Recovery Contract Assessment

## Objective

Define alternatives for explicit, attempt-scoped recovery and separation from
ordinary QueueManager processing.

## Architectural Context

OWNER-DECISION-011 requires an explicit recovery boundary. Objective identity
now canonically identifies one attempt and is propagated to Plan and QueueItem.
The remaining ambiguity is which failed/pending work recovery selects, who owns
Objective lifecycle, and how ordinary processing avoids implicit continuation.

## In Scope

- inspect QueueManager, DefaultWorker, Task, ExecutionEngine, and
  ExecutionManager state ownership;
- define recovery preconditions, eligibility, reset, ordering, and persistence;
- define ordinary-processing separation without blocking unrelated attempts;
- compare coherent recovery alternatives and request an owner decision.

## Non-Goals

- product code, tests, entities, registries, APIs, or schemas;
- active-data migration or legacy association;
- automatic retry, retry limits, backoff, scheduling, or provider fallback;
- CLI, Kernel, UI, deployment, credentials, or unrelated findings.

## Verification Requirements

- use Objective ID as the only attempt selector;
- preserve completed work and unrelated attempts;
- specify fail-fast and original-exception behavior during recovery;
- keep lifecycle ownership outside QueueManager;
- keep unidentified legacy attempts non-recoverable without inference;
- validate JSON, whitespace, secrets, scope, and runtime-data preservation.

## Stop Condition

Stop after proposal, decision request, verification, and handoff are recorded
and pushed. Do not select or implement recovery.
