# WO-115 — Opt-In Executive Composition Assessment

Baseline: 5f3fc5d, feat/operational-builder-chain, 2026-09-03.
Objective: define the smallest explicit composition boundary for the verified
Python-file capability and skill routing. Scope is proposal and evidence only;
no source, provider, schema, registration or executable-authority changes.

## Evidence and limitation

`create_executive` already owns isolated CapabilityRegistry, SkillRegistry,
AgentRegistry and WorkerRegistry. It registers SystemCapability and the planning
skill only. SkillResolver now supports explicit routes, but this factory still
uses legacy resolution. OperationalSession constructs the factory without an
executable option. ExecutivePipeline always invokes PlannerManager.plan, and
the default generator produces description-only Tasks.

Thus capability composition and application-facing Task submission are separate
gaps. This proposal addresses composition only. It must not claim an end-to-end
CLI builder or bypass the planner by changing persisted Plans behind its back.

## Option A — Optional output workspace on create_executive (recommended)

Add a keyword-only `python_file_workspace=None` argument to the existing
factory. Omission preserves the complete current graph and legacy routing.
When supplied:

1. Validate an explicitly supplied existing output directory before constructing
   the enabled graph; never infer it from cwd, globals, credentials or a model.
2. Retain the ordinary SystemCapability and planning skill.
3. Register one PythonFileCapability bound to that output directory and one
   corresponding skill in this factory instance's private registries only.
4. Construct SkillResolver with `python_file -> python-file` and explicit
   default `planning`. No other executable intent type is enabled.
5. Keep stores/state ownership independent from the output-directory argument;
   supplying it does not move state or grant access outside the capability's
   existing output confinement. No directories are created by configuration.
6. Factory construction must not execute a task or create output files.
7. Do not propagate this argument through OperationalSession or CLI yet; that
   requires a separate contract for creating/submitting an executable Task.

Consequence: authorization is explicit per Executive instance, using existing
composition ownership. The option is intentionally narrow rather than an
arbitrary plugin/capability injection API.

## Alternatives

Option B: register PythonFileCapability by default or globally. Reject: this
silently expands authority and loses per-workspace opt-in.

Option C: duplicate create_executive in a separate builder factory. Reject for
this increment: it duplicates the large ownership graph and risks drift.

## Acceptance boundary if approved

A separate work order modifies executive/factory.py and focused factory tests,
plus control-plane records. Verify omission compatibility, exact enabled
capability/skill/resolver composition, ordinary-task routing in enabled mode,
typed-task selection of the confined capability, two-instance isolation,
invalid-workspace rejection and construction without file writes. Reuse the
existing capability and routing tests; do not claim that inspection of factory
wiring alone proves application-facing executable submission.

Run focused/full tests, compile/import checks, architecture inspection and
active-data preservation checks. No planner/session/CLI changes, new task kinds,
model/provider use, shell/Git authority, or print-only restriction relaxation.

## Owner decision requested

Approve, revise or reject **Option A: explicit python_file_workspace opt-in on
create_executive**, with the seven rules and acceptance boundary above.

Assessment complete. No tests were rerun for this documentation-only work;
the 206-test result remains the WO-114 baseline. Unrelated edits are preserved.
