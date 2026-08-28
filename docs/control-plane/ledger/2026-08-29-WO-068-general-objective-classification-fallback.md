# WO-068 — General Objective Classification Fallback

## Objective

Implement OWNER-DECISION-007 and resolve FINDING-032 with deterministic
canonical fallback classification.

## Architectural Context

Fallback belongs to classifier resolution, not ExecutivePipeline. The canonical
default classifier owns the `general_objective` policy; independently composed
classifiers retain explicit caller-selected behavior.

## Scope

- Add optional fallback construction to IntentClassifier.
- Return that fallback only after every explicit rule misses.
- Configure `create_default_classifier()` with `general_objective`.
- Verify explicit-rule precedence, canonical fallback, custom opt-in, and
  operational-session behavior.

## Explicit Non-Goals

- No pipeline branching, routing, authorization, skill, council, provider,
  model, credential, CLI syntax, Content OS, fallback execution, retry,
  deployment, or schema change.

## Verification Requirements

- Focused classifier, application, CLI, and Executive-factory tests.
- Full pytest, import sweep, compile, and architecture inspection.
- Active-data, project-state JSON, secret, whitespace, and scope checks.

## Stop Condition

Stop after FINDING-032 is resolved, independently reviewed, recorded, and
pushed. Do not introduce classification-driven routing.
