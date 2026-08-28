# WO-067 — Unclassified Objective Policy Decision

## Objective

Resolve the architectural ambiguity in FINDING-032 by obtaining an owner choice
for unmatched classifier results before changing classifier or pipeline code.

## Architectural Context

IntentClassifier returns `None` when no keyword matches. ExecutivePipeline
records that value but does not use classification for delegation, planning,
or execution. The current keyword catalogue is descriptive and incomplete; it
is not an established authorization gate.

## Scope

- Inspect classifier, Executive pipeline, result, CLI, and tests.
- Record bounded policy options and a recommendation.
- Update current state and handoff records.

## Explicit Non-Goals

- No classifier, pipeline, result, CLI, test, provider, model, credential,
  Content OS, fallback, retry, deployment, or schema change.

## Verification Requirements

- Confirm current unmatched behavior and downstream consumers.
- Confirm classification does not currently select execution behavior.
- Validate project-state JSON, whitespace, secret, scope, and active-data
  boundaries.

## Stop Condition

Stop after DECISION-REQUEST-007 is published. Policy implementation requires
the owner's explicit option selection.
