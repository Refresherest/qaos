# WO-065 — One-Shot CLI Objective Adapter

## Objective

Implement OWNER-DECISION-006 as the first user-facing adapter over
OperationalSession.

## Architectural Context

The CLI must remain a presentation adapter. OperationalSession retains
workspace, canonical Objective, Executive, and Kernel lifecycle ownership.
The legacy command registry must not gain an import cycle through Kernel.

## Scope

- Add `python -m qaos.main objective --workspace <path> <goal...>`.
- Require a non-empty explicit workspace and goal.
- Delegate exactly once to OperationalSession.
- Print objective, status, classification, and assignee summary fields.
- Return status 0 for completed execution, 1 for execution failure, and 2 for
  invalid objective-command usage.
- Preserve existing command behavior and help output while listing objective.

## Explicit Non-Goals

- No implicit active-data workspace, interactive mode, history, Content OS,
  provider, model, credential, fallback, retry, deployment, remote execution,
  schema, Kernel, Runtime, Executive, or OperationalSession change.

## Verification Requirements

- Focused CLI, application-session, and Executive-factory tests.
- Subprocess proof against an isolated temporary workspace.
- Full pytest, import sweep, compile, and architecture inspection.
- Active-data, project-state JSON, secret, whitespace, and scope checks.

## Stop Condition

Stop after the one-shot adapter is implemented, independently reviewed,
recorded, and pushed. Do not add interactive mode or Content OS wiring.
