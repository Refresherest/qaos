# WO-111 — Implement Approved Executable Task

Authority: OWNER-DECISION-021. Baseline: f461906 on
feat/operational-builder-chain, 2026-09-03.

Objective: implement the first Task-owned typed intent that atomically creates
one Python file and verifies exact output through direct current-Python
invocation in an explicit disposable workspace.

In scope: Task serialization compatibility, typed intent, specifically
registered capability, focused tests, regression/compile/import/architecture
checks, and evidence records. Non-goals are the exclusions in
OWNER-DECISION-021, default-runtime registration, planner generation, CLI/API
expansion, recovery redesign and active-data changes.

Stop when the ten WO-109 rules are verified or contrary evidence blocks safe
implementation.
