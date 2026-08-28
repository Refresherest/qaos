# WO-058 — Explicit Runtime Integration Proof

## Objective

Prove that existing explicitly composable QAOS services execute one canonical
Objective end-to-end through Kernel using one isolated Stores workspace.

## Architectural Context

WO-038 through WO-057 established explicit boundaries from Kernel and Executive
Pipeline through planning, execution, workers, agents, skills, capabilities,
reflection, and learning. No single test had exercised the real chain together.

## Requirements

1. Compose the existing runtime without a new production factory or abstraction.
2. Execute a canonical Objective through Kernel and the real ExecutivePipeline.
3. Prove classification, delegation, planning, queue execution, reflection, and
   learning complete against one selected Stores workspace.
4. Prove all planned tasks and QueueItems complete.
5. Record any lifecycle inconsistency without fixing it in this verification scope.

## Scope

- One full explicit-runtime integration test
- Integration evidence and any resulting finding
- Verification, current-state, and handoff records

## Explicit Non-Goals

- No production composition factory or runtime API.
- No objective lifecycle, failure, retry, provider, model, credential, or
  Content OS behavior change.

## Verification Requirements

- Run the integration test with focused related tests.
- Run full regression, import sweep, compilation, architecture inspection, and
  active-data comparison.

## Stop Condition

Stop after the integration proof and any limitation are independently reviewed
and WO-058 is published.
