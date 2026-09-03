# WO-114 — Explicit Skill Routing Implementation

Baseline: 85f3c74, feat/operational-builder-chain. Authority:
OWNER-DECISION-022. Objective: implement immutable, explicit intent-type routes
in SkillResolver while retaining legacy construction behavior.

Scope: resolver, focused composition tests and control-plane evidence only.
No factory/session/CLI changes, capability registration, new executable types,
providers, credentials, schema or active-data changes.

Verify deterministic exact routing, missing/unknown route rejection before
execution, copied immutable configuration, legacy compatibility, regressions,
compile/import checks and architecture inspection. Stop at verified completion.
