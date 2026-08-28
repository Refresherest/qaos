# OWNER-DECISION-007 — Unclassified Objective Policy

## Status

`ACCEPTED`

## Decision

The owner selected **Option B — Assign `general_objective` and Continue** from
DECISION-REQUEST-007.

The canonical default classifier must return `general_objective` only when no
explicit keyword rule matches. Explicit matches retain precedence. The fallback
does not designate or select a skill, council member, provider, or model.

Custom IntentClassifier instances retain caller control and must not receive
the canonical fallback unless explicitly configured with one.
