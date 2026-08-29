# WO-085 — Record Objective Identity Propagation Decision

## Objective

Record the owner's Option A selection from DECISION-REQUEST-014 as the governing
Plan and QueueItem Objective-identity propagation contract.

## Architectural Context

Objective owns canonical execution-attempt identity. WO-083 implements that
foundation; WO-084 assesses how Plan and QueueItem reference it without taking
ownership or inventing legacy associations.

## In Scope

- resolve DECISION-REQUEST-014;
- record OWNER-DECISION-014;
- update FINDING-036 and current project state;
- verify and hand off the documentation-only checkpoint.

## Non-Goals

- product code, tests, entities, registries, schemas, or active data;
- migration, legacy association, recovery, filtering, continuation, or guards;
- credentials, providers, models, OpenHands profiles, or deployment.

## Verification Requirements

- control-plane JSON parses;
- documentation diff passes whitespace and scoped-secret checks;
- only the explicitly scoped files are staged;
- runtime data and unrelated working-tree changes remain untouched.

## Stop Condition

Stop after the decision is verified, committed, pushed, and handed off.
Implementation requires its own bounded work order.
