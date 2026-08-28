# WO-050 — Classifier Stage Composition

## Objective

Allow an explicitly composed classifier stage to retain a caller-selected
IntentClassifier-compatible service without mutating module state.

## Architectural Context

IntentClassifier already owns instantiable rule state and ExecutivePipeline
already accepts a classifier-stage dependency. ClassifierManager was the sole
remaining implicit boundary between them.

## Requirements

1. ClassifierManager accepts an explicit classifier service.
2. Classification delegates to the selected service unchanged.
3. The default constructor retains the existing module classifier.
4. No rule, matching, or result-contract changes.

## Scope

- ClassifierManager dependency injection
- Explicit and default compatibility tests
- Finding, verification, current-state, and handoff records

## Explicit Non-Goals

- No classifier registry or built-in rule changes.
- No persistence, provider, model, credential, Content OS, or other stage change.

## Verification Requirements

- Prove an isolated rule set is selected without default-rule leakage.
- Prove default service compatibility.
- Run focused and full regression checks, import sweep, compilation,
  architecture inspection, and active-data comparison.

## Stop Condition

Stop after FINDING-023 is independently reviewed and WO-050 is published.
