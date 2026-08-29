# WO-079 — Execution-Attempt Identity Design

## Objective

Design alternatives for canonical execution-attempt identity required by
OWNER-DECISION-011 without changing code or persisted schemas.

## Scope

- Inspect Objective, Plan, Task, QueueItem, OperationalSession, ExecutionEngine,
  managers, registries, and JSON projections.
- Identify the closest existing source-of-truth concept.
- Compare three identity ownership alternatives.
- Define compatibility and non-inference constraints.
- Produce a recommendation and owner decision request.

## Explicit Non-Goals

- No product code, tests, entity, registry, API, schema, storage collection,
  migration, ID generation, recovery, retry, continuation guard, provider,
  model, credential, Content OS, fallback execution, or deployment change.

## Verification Requirements

- Trace creation and persistence through the active execution path.
- Check for an existing canonical ID abstraction or attempt domain.
- Identify duplicate-concept and source-of-truth risks.
- Validate project-state JSON, whitespace, secret, and scope boundaries.

## Stop Condition

Stop after the proposal, decision request, verification, and handoff are
recorded and pushed. Do not select or implement an identity design.
