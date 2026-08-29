# WO-090 — Record Task Identity Decision

## Objective

Record the owner's Option A selection from DECISION-REQUEST-016 as the governing
Task identity and QueueItem action-reference contract.

## Architectural Context

FINDING-037 proves that durable recovery cannot keep Plan and Queue Task state
coherent after reload without canonical Task correlation.

## In Scope

- resolve DECISION-REQUEST-016;
- record OWNER-DECISION-016;
- update FINDING-037 and current project state;
- verify and hand off the documentation-only checkpoint.

## Non-Goals

- product code, tests, entities, APIs, schemas, or active data;
- recovery, migration, legacy association, QueueItem identity, or retry policy;
- Kernel, CLI, UI, providers, models, credentials, or deployment.

## Verification Requirements

- control-plane JSON parses;
- documentation passes whitespace and scoped-secret checks;
- only explicitly scoped files are staged;
- runtime data and unrelated working-tree changes remain untouched.

## Stop Condition

Stop after the decision is verified, committed, pushed, and handed off. Task
identity implementation requires its own bounded work order.
