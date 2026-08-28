# WO-042 — Executive Invocation Boundary Decision

## Objective

Characterize the unresolved Kernel/CLI executive invocation boundary and request
one owner decision without changing product code or existing command semantics.

## Architectural Context

Runtime can retain an explicit executive service and Kernel can use an isolated
dispatcher. No established invocation contract connects them. The existing
`run <member>` command belongs to Council-member execution, while the executive
service accepts a canonical Objective.

## Scope

- Record FINDING-017 and DECISION-REQUEST-003.
- Compare bounded invocation options and recommend one.
- Update current state, project state, verification, and handoff records.

## Explicit Non-Goals

- Do not add, rename, or repurpose a CLI command.
- Do not change Kernel, Runtime, Dispatcher, Council, Objective, or Executive code.
- Do not implement a second Content OS slice or change providers or credentials.

## Acceptance Criteria

1. Existing `run` and executive input contracts are distinguished explicitly.
2. Options identify input, ownership, persistence, and compatibility consequences.
3. One option is recommended without being implemented or treated as approved.
4. Product code, tests, active data, and unrelated work remain unchanged.

## Stop Condition

Stop after publishing the decision request. No invocation implementation begins
until the owner selects an option.
