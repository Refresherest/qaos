# WO-069 — General Objective CLI Smoke

## Objective

Verify OWNER-DECISION-007 through the real one-shot CLI using an unmatched goal
in a fresh disposable workspace.

## Scope

- Capture the active-data baseline.
- Run one CLI objective against `.qaos-smoke-069` with a goal matching no
  explicit classifier keyword.
- Verify CLI classification, exit status, and persisted lifecycle evidence.
- Remove the disposable workspace after inspection.

## Explicit Non-Goals

- No product code, test, classifier, pipeline, schema, provider, model,
  credential, Content OS, fallback execution, retry, or deployment change.

## Verification Requirements

- Fresh target absent before execution.
- CLI reports `general_objective` and exits 0.
- One completed objective, five completed tasks, and six completed queue items.
- One reflection, memory, and knowledge record.
- Active JSON hashes and timestamps unchanged.
- Disposable workspace removed.

## Stop Condition

Stop after the smoke evidence is reviewed, recorded, and pushed.
