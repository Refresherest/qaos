# WO-017 — OpenHands Inherited-Model Smoke Test

## Objective

Make the QAOS CSA -> PE -> Reviewer smoke test executable in OpenHands Cloud
despite the delegated sub-agent profile store reporting no named profiles.

## Architectural Context

OpenHands file-based agents support `model: inherit`, which uses the parent
conversation LLM. The prior SMOKE-001 result established that the project
agent files were discovered but named model profiles could not be resolved by
the delegated runtime. This work order therefore proves orchestration only.

## Scope

- Change the six QAOS OpenHands sub-agents to `model: inherit`.
- Update the Builder Chain document to state the temporary operating mode and
  its limits.
- Run one no-change CSA -> PE -> Reviewer smoke test using a parent profile
  already shown to work in OpenHands.

## Explicit Non-Goals

- Do not create, alter, or expose credentials.
- Do not claim model validation or designation.
- Do not configure an ordered multi-model fallback chain.
- Do not modify QAOS product code, tests, or unrelated files.

## Acceptance Criteria

1. All six agent files specify `model: inherit`.
2. The Builder Chain document distinguishes inherited-model orchestration proof
   from independent model routing.
3. SMOKE-001 reaches CSA, PE, and Reviewer without repository changes.
4. The reviewer returns a verdict and the working tree remains clean.

## Stop Condition

Stop after the first complete smoke-test result. Treat any separate-model
routing work as a future owner-authorized work order.
