# WO-078 — Record Explicit Recovery Direction

## Objective

Record OWNER-DECISION-011 without prematurely designing or implementing
execution-attempt identity or recovery behavior.

## Architectural Context

WO-077 proves ordinary repeat-call continuation. Objective, Plan, and QueueItem
currently lack a canonical attempt/batch identity. The selected direction
therefore requires a separate design before safe enforcement.

## Scope

- Record OWNER-DECISION-011.
- Mark DECISION-REQUEST-011 resolved.
- Preserve FINDING-036 as open pending design and implementation.
- Record the next bounded design-assessment step.

## Explicit Non-Goals

- No product code, tests, entities, schemas, migration, recovery API, retry,
  continuation guard, dependency behavior, provider, model, credential,
  Content OS, fallback execution, or deployment change.

## Verification Requirements

- Confirm the decision matches selected Option A.
- Confirm current entity and persistence contracts remain unchanged.
- Validate project-state JSON, whitespace, secret, and scope boundaries.

## Stop Condition

Stop after the direction is independently reviewed, recorded, and pushed. Do
not design attempt identity in this work order.
