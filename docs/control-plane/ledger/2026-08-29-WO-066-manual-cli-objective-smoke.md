# WO-066 — Manual CLI Objective Smoke

## Objective

Run one owner-approved manual one-shot CLI objective against a fresh disposable
workspace and verify the persisted operational result without touching active
QAOS data.

## Scope

- Capture the active-data hash and modification-time baseline.
- Run exactly one `qaos.main objective` command against
  `.qaos-smoke-066`.
- Inspect all generated JSON records and the process exit status.
- Record any unrelated behavior as a separate finding.
- Remove the disposable workspace after evidence capture.

## Explicit Non-Goals

- No product code, test, schema, provider, model, credential, classifier,
  fallback, retry, deployment, Content OS, or active-data change.

## Verification Requirements

- Fresh target absent before execution.
- Exit status 0 and completed objective lifecycle.
- Five completed planned tasks and six completed queue items.
- Reflection, memory, and knowledge evidence persisted.
- Active JSON hashes and timestamps unchanged.
- Disposable workspace removed after inspection.

## Stop Condition

Stop after the smoke evidence, finding, verification, and handoff are recorded
and pushed. Do not repair newly discovered policy questions.
