# WO-072 — OperationalSession Pending Failure

## Objective

Implement OWNER-DECISION-008 and resolve FINDING-033 without changing
ExecutionManager lifecycle ownership.

## Architectural Context

OperationalSession owns Objective creation before Kernel invocation.
ExecutionManager owns lifecycle after it starts. The application boundary may
therefore fill only the conditional pre-execution gap.

## Scope

- Catch exceptions escaping Kernel from `execute_goal`.
- If the created Objective is still pending, fail and persist it through the
  session's shared ObjectiveManager.
- Re-raise the original exception.
- Do not repeat or overwrite downstream failure transitions.
- Verify persisted timestamps, exception identity, and conditional ownership.

## Explicit Non-Goals

- No Kernel, Executive, ExecutionManager, ObjectiveManager, schema, persisted
  error, post-execution failure, retry, recovery, Content OS, provider, model,
  credential, fallback execution, or deployment change.

## Verification Requirements

- Focused application, execution-manager, and CLI tests.
- Full pytest, import sweep, compile, and architecture inspection.
- Active-data, project-state JSON, secret, whitespace, and scope checks.

## Stop Condition

Stop after FINDING-033 is resolved, independently reviewed, recorded, and
pushed.
