# WO-048 — Reloaded Reflection Learning Identity

## Objective

Allow Learner to process persisted/reloaded reflections whose objective identity
is a string, consistently with the existing LearningEngine contract.

## Architectural Context

Reflection persistence stores objective identity as its canonical goal string.
LearningEngine normalizes Objective objects and strings, but Learner's diagnostic
message accessed `.goal` directly and failed before delegation after reload.

## Requirements

1. Learner derives a diagnostic goal from Objective `.goal` or string identity.
2. The original Reflection is passed to the selected LearningEngine unchanged.
3. Return values and live canonical Objective behavior remain unchanged.
4. No reflection rehydration, schema, registry, or persistence change.

## Scope

- Learner diagnostic identity normalization
- Persist, reload, and learn regression test
- Finding, verification, current-state, and handoff records

## Explicit Non-Goals

- No Objective lookup or rehydration.
- No ReflectionManager, LearningEngine, or persistence schema change.
- No other executive stage, Content OS, provider, model, or credential change.

## Acceptance Criteria

1. A reloaded string-identity Reflection reaches the selected engine unchanged.
2. Diagnostic output contains the persisted goal without AttributeError.
3. Canonical live behavior and full verification remain green.
4. Active data remains unchanged.

## Stop Condition

Stop after FINDING-021 is independently reviewed and published.
