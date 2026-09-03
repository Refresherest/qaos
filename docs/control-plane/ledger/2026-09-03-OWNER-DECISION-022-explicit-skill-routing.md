# OWNER-DECISION-022 — Explicit Skill Routing

Date: 2026-09-03. Authority: Qaasim April, repository owner.

The owner selects WO-112 Option A: explicit intent-type skill routes.
All five resolution rules and the stated acceptance boundary are approved.

SkillResolver will accept an injected immutable intent-type-to-skill-name
mapping and an explicit default skill for Tasks without intent. Explicit
routing must fail closed for missing defaults, routes, unknown types or missing
skills, before capability execution. Description parsing and insertion-order
routing are excluded from this mode. Existing construction without injected
routes retains first-skill compatibility.

A separate implementation work order may change SkillResolver and focused
composition tests only, plus verification/control-plane records. It must prove
deterministic routing, rejection before execution, legacy compatibility and
unchanged default executive/session behavior.

This does not authorize production registration of PythonFileCapability,
an executable OperationalSession method, new providers, shell/Git authority,
or expansion of the print-only executable intent.
