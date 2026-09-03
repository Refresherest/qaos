# OWNER-DECISION-023 — Opt-In Executive Composition

Date: 2026-09-03. Authority: Qaasim April, repository owner.

The owner selects WO-115 Option A and approves its seven rules and acceptance
boundary: add keyword-only `python_file_workspace=None` to create_executive.

Omission retains current composition and legacy routing. An explicitly supplied
existing output directory enables one instance-local PythonFileCapability and
python-file skill, with explicit python_file routing and planning as default.
The ordinary system capability remains. Validate the directory before enabled
graph construction; do not infer or create it. Configuration must not execute
tasks, create output files, move persisted state or mutate global registries.

A separate implementation work order may modify executive/factory.py, focused
factory tests and verification/control-plane records. It must prove omission
compatibility, exact enabled wiring, ordinary and typed routing, two-instance
isolation, invalid-directory rejection, construction without writes, regression
safety and active-data preservation.

OperationalSession, CLI, planner submission, new executable intent types,
model/provider selection, shell/Git authority and relaxation of the print-only
fixture remain excluded. This is composition approval, not an end-to-end CLI
builder or application-facing executable submission contract.
