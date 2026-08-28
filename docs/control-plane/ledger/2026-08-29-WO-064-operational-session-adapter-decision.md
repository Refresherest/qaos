# WO-064 — Operational Session Adapter Decision

## Objective

Choose the first user-facing adapter over OperationalSession before changing
the existing CLI or introducing another interface.

## Architectural Context

WO-063 provides a tested programmatic application lifecycle. The existing CLI
is a legacy command dispatcher with no workspace-selection, objective-output,
or exit-status contract. An adapter must not silently write active repository
data or duplicate application composition.

## Scope

- Inspect existing CLI, command registry, packaging, and OperationalSession.
- Record bounded adapter alternatives and a recommendation.
- Update current state and handoff records.

## Explicit Non-Goals

- No CLI, command, application, product, test, Content OS, provider, model,
  credential, fallback, retry, deployment, remote execution, or schema change.

## Verification Requirements

- Confirm no current OperationalSession adapter exists.
- Confirm the existing CLI lacks explicit workspace and objective contracts.
- Validate project-state JSON, whitespace, secret, scope, and active-data
  boundaries.

## Stop Condition

Stop after DECISION-REQUEST-006 is published. Adapter implementation requires
the owner's explicit option selection.
