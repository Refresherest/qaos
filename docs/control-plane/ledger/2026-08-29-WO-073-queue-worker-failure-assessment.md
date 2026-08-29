# WO-073 — Queue-Worker Failure Assessment

## Objective

Identify and reproduce the next highest-priority operational lifecycle gap
after resolving pre-execution Objective failure ownership.

## Scope

- Inspect QueueManager, DefaultWorker, Agent, Skill, Capability, and Task
  lifecycle and persistence boundaries.
- Run one isolated delegated-worker failure probe.
- Record one bounded finding and owner-decision boundary.
- Remove the disposable probe workspace.

## Explicit Non-Goals

- No product code, tests, lifecycle, error-detail, schema, retry, recovery,
  provider, model, credential, Content OS, fallback execution, or deployment
  change.

## Verification Requirements

- Reproduce the exception and compare live, persisted, and reloaded state.
- Distinguish QueueItem lifecycle from Task lifecycle and persistence.
- Confirm active data remains unchanged and remove the probe workspace.
- Validate project-state JSON, whitespace, secret, and scope boundaries.

## Stop Condition

Stop after the assessment, finding, decision request, verification, and handoff
are recorded and pushed. Do not select or implement failure ownership.
