# WO-147 — Broader Builder Milestone Assessment

2026-09-04; baseline 293bc71; feat/operational-builder-chain.
Authority: owner proceed on HANDOFF-126. Scope: evidence-backed milestone/options
and current-state/handoff records only. No infrastructure or product changes.
Stop for owner decision; rollback is owner-directed record revision only.

## What is actually proven

WO-145: 450 regressions, 198 imports, controlled-language preview with no build
authority. WO-146: ten operator phases and 143 focused regressions. The builder
assembles a reviewed four-file application with seven bounded output selections;
it verifies, publishes without overwrite and retains lifecycle evidence.
This is useful groundwork, not arbitrary application design or code generation.
Further synonyms or metric combinations would not close that larger gap.

## Executable evidence and ownership

- capabilities/python_project.py checks exact trusted member bytes and invokes
  sys.executable through subprocess.run in the staging directory. It supplies
  timeouts and fixed test expectations, not a separate execution identity or
  general network/filesystem isolation boundary.
- capabilities/python_file.py likewise uses direct subprocess execution for its
  restricted approved intent. Do not relax intent/source restrictions to accept
  generated code merely because the executor can launch Python.
- planner/intents.py and planner/controlled_brief.py carry bounded intent and
  grammar, not a general requirements specification or generated-code contract.
- ai/provider.py is a generate interface; ai/providers/mock.py returns mock text.
  Their existence does not designate a production code-generation model.
- artifacts/artifact.py and manager.py provide existing artifact ownership and
  persistence. Any future candidate/evidence representation must reconcile these
  existing concepts before introducing a new registry or data model.

Inspection found no isolated arbitrary-code runner in these paths. This does not
claim that no suitable host/runtime exists outside the repository: host inventory
has not been performed in this work order. OpenHands startup remains a separately
recorded blocker; no fresh external diagnosis or provider-readiness claim is made.

## Gaps that must remain distinct

1. Requirements understanding and independently stated acceptance criteria.
2. Candidate source generation, model designation and traceable provenance.
3. Isolated validation of candidate code, including resource and data boundaries.
4. Approval/promotion of verified output, with revision and failure handling.

These are separate authorities. A plausible candidate is not approved code; a
passing test is not permission to publish; provider access is not designation.

## Option A — Isolated generated-code validation milestone (recommended)

Prioritize an execution boundary before allowing arbitrary candidate code. The
milestone should eventually demonstrate that a reviewed fixed candidate can be
tested with independent acceptance in a disposable isolated environment, while
bounded negative probes cannot reach forbidden resources. Do not attach a model
or arbitrary-code input to the existing trusted runner to get there.

Approval of A authorizes only the following first work package: a read-only
feasibility assessment and implementation-ready gate proposal, not provisioning
or untrusted execution. Inventory relevant local runtime availability, versions,
host prerequisites and existing repository integration seams. Use narrowly scoped
read-only version/status checks; do not launch stopped services, enumerate secrets,
contact paid accounts or inspect unrelated user data. If checks require additional
system permissions, request them explicitly. No runtime is selected by this record.

Compare available approaches only after that evidence. Record candidate controls
for: denied outbound network, no inherited credentials, no repository/home mounts,
explicit read-only inputs, confined disposable writes, process-tree termination,
CPU/memory/time/process/output/storage bounds, and cleanup/reproducible reset.
Keep host ownership, cost, installation requirements and unsupported guarantees
explicit. Name precise independently authored acceptance and negative tests for
each claimed control. A timeout, subprocess flag or directory check alone is not
evidence of these controls.

The first gate must produce:

- A dated environment inventory with exact non-secret commands/results, including
  unavailable/blocked checks rather than inferred readiness.
- A proposed input/output/evidence contract and ownership map to current domains,
  distinguishing candidate bytes, acceptance tests, results and promotion authority.
- A platform recommendation (or explicit no-feasible-option result), prerequisite
  actions, cost/permission questions, and an owner decision request before setup.
- A staged test plan: harmless smoke first; bounded reviewed negative probes only
  after the isolation configuration is separately approved and established.
- Fail-closed behavior for missing controls and a stop/cleanup policy. No automatic
  fallback to direct host execution. Preserve the existing trusted builder unchanged.

Subsequent installation, container/image download, VM/cloud creation, account use,
network policy changes, external spend, runner implementation and probe execution
all require separate scoped authorization. A is not approval for any of them.
No GPU requirement is introduced. Candidate generation and model designation remain
later independent decisions; the validation contract need not depend on a provider.

This first step is an enabling assessment, not a new end-user app feature. Its
value is resolving the concrete execution prerequisite for broader code building.

## Alternatives

Option B: model-assisted candidate generation without execution. Closer to visible
code output, but requires model/data/acceptance decisions and leaves executable
validation unresolved. Candidate text must not be automatically executed or promoted.

Option C: a second, materially different trusted application template. Provides
another usable deterministic app within current constraints, but does not establish
general code generation or isolation. App behavior and persistence would need a
separate proposal; no specific application is silently selected here.

## Decision and verification

Approve, revise or reject Option A's milestone direction and read-only first gate.
No architecture implementation or infrastructure change is authorized by this
proposal. Architecture-awareness identified execution ownership and preserved
trusted-code restrictions rather than reusing them as an untrusted runner.

Evidence: read-only source/ledger inspection and scoped path search. No runtime
tests or architecture tool rerun for documentation only; prior verification is
attributed above. JSON/whitespace checks apply to records. Product source, tests,
active data, dirty skills, untracked configuration/drafts/tools/test folders and
credentials/providers remain unchanged. This is not a security audit or proof
that any proposed isolation technology is secure.
