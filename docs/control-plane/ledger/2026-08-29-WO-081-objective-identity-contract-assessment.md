# WO-081 — Objective Identity Contract Assessment

## Objective

Define alternatives for opaque ID generation, ObjectiveRegistry compatibility,
and legacy Objective loading under OWNER-DECISION-012.

## Scope

- Inspect Objective construction, manager load/create/register/save, registry
  lookup, caller expectations, and existing tests.
- Define canonical and compatibility lookup behavior.
- Define legacy missing-ID behavior without migration inference.
- Compare three coherent contract alternatives.
- Produce a recommendation and owner decision request.

## Explicit Non-Goals

- No product code, tests, entity, registry, API, schema, ID generator,
  migration, propagation, recovery, retry, guard, provider, model, credential,
  Content OS, fallback execution, or deployment change.

## Verification Requirements

- Account for repeated equal goals without breaking current goal lookups.
- Preserve deterministic testability and explicit source-of-truth ownership.
- Prohibit inferred identity for legacy records.
- Validate project-state JSON, whitespace, secret, and scope boundaries.

## Stop Condition

Stop after the proposal, decision request, verification, and handoff are
recorded and pushed. Do not select or implement the contract.
