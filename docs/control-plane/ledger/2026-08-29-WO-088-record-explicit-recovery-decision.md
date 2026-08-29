# WO-088 — Record Explicit Recovery Decision

## Objective

Record the owner's Option A selection from DECISION-REQUEST-015 as the governing
explicit recovery and ordinary-processing separation contract.

## Architectural Context

Objective identity now correlates one failed attempt across Objective, Plan,
and QueueItem. OWNER-DECISION-011 requires recovery to be explicit rather than a
repeated ordinary queue call.

## In Scope

- resolve DECISION-REQUEST-015;
- record OWNER-DECISION-015;
- update FINDING-036 and current project state;
- verify and hand off the documentation-only checkpoint.

## Non-Goals

- product code, tests, APIs, entities, schemas, or active data;
- migration, legacy association, automatic retry, retry policy, or audit;
- Kernel, CLI, UI, providers, models, credentials, or deployment.

## Verification Requirements

- control-plane JSON parses;
- documentation passes whitespace and scoped-secret checks;
- only explicitly scoped files are staged;
- runtime data and unrelated working-tree changes remain untouched.

## Stop Condition

Stop after the decision is verified, committed, pushed, and handed off.
Implementation requires its own bounded work order.
