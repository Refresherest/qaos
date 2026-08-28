# WO-063 — Operational Application Session

## Objective

Implement OWNER-DECISION-005 as one reusable, provider-neutral application
lifecycle above the verified Executive factory and Kernel.

## Architectural Context

The application boundary must preserve Kernel's canonical-Objective contract
while guaranteeing that objective creation and lifecycle persistence use the
same explicit ObjectiveManager and Stores workspace.

## Scope

- Add public `qaos.application.OperationalSession`.
- Require one explicit Stores instance.
- Accept optional explicit Configuration and logger collaborators.
- Compose one shared ObjectiveManager, Executive, and Kernel.
- Add `execute_goal(goal)` with deterministic type, emptiness, and whitespace
  validation.
- Verify successful execution, persistence, isolation, and invalid inputs.

## Explicit Non-Goals

- No CLI, command registry, Kernel, Runtime, Executive, Content OS, provider,
  model, credential, fallback, retry, deployment, remote execution, or schema
  change.

## Verification Requirements

- Focused application, Executive-factory, and Kernel/CLI tests.
- Full regression suite and complete package import sweep.
- Compile and architecture inspection.
- Active-data, project-state JSON, secret, whitespace, and scope checks.

## Stop Condition

Stop after the application session is implemented, independently reviewed,
recorded, and pushed. Do not add a CLI adapter.
