# WO-118 — Application Intent Submission Assessment

Baseline 99d67f9, feat/operational-builder-chain, 2026-09-03.
Objective: propose explicit application submission of the approved typed intent.
Scope is assessment/decision request only; no source or runtime authority changes.

## Evidence

OperationalSession creates and validates canonical session-owned Objectives.
create_executive can opt into confined Python-file execution, but the session
does not expose that option. ExecutivePipeline always calls PlannerManager.plan;
the default generator creates description-only Tasks. Merely registering a
capability therefore cannot create a meaningful executable workload.

## Option A — Explicit session submission, existing pipeline (recommended)

1. Add optional python_file_workspace to OperationalSession construction and
   forward it to the approved factory. Omission retains current behavior.
2. Add `execute_intent(objective, intent)` to OperationalSession. Accept only
   the exact canonical Objective already registered in that session, still
   pending, and the currently supported validated PythonFileIntent. Require
   explicit workspace opt-in. The caller uses existing create_objective first,
   so identity is available even if execution subsequently fails.
3. Reject wrong ownership/status, unsupported intent, disabled capability or an
   existing Plan before changing execution state. Never replace a Plan or reuse
   this method as recovery. Existing explicit recovery remains separate.
4. Delegate through a narrow ExecutiveManager.execute_intent method, using the
   same orchestrator and six-stage pipeline. Pass intent explicitly for that
   call only; do not attach transient attributes to Objective, alter its schema,
   mutate global configuration or create a second orchestration graph.
5. At the planning stage only, invoke a new PlannerManager method that creates
   one Plan with one canonical Task carrying the supplied intent. PlannerManager
   assigns Task identity and persists it using its existing ownership. Ordinary
   planning stays unchanged; no prewritten JSON or private-registry manipulation.
6. Execution, routing, output confinement, bounded evidence, reflection and
   learning use the existing composed services. ExecutionManager still owns
   Objective start/complete/fail; the session retains its pending-failure guard
   for failures before execution. Preserve original exception propagation.
7. Return the existing ExecutionResult, including Plan and execution report;
   do not add a competing result or task identity concept. One executable Plan
   Task does not imply only one QueueItem: ordinary Council delegation remains.
8. Kernel's existing execute_objective contract and the CLI remain unchanged.
   The new explicit application path delegates to Executive directly, as a
   deliberately approved boundary—not an implicit expansion of the ordinary
   Kernel command. No natural-language inference or automatic executable planning.

This accepts a narrow new session-to-Executive entry point while reusing the
existing orchestration and ownership graph. It intentionally does not introduce
a generic plan-submission API, arbitrary Task lists or new intent types.

## Alternatives

Option B: extend Kernel.execute_objective with executable intent and propagate
that contract through normal invocation. More uniform entry, but broadens the
Kernel's approved canonical-Objective-only contract and its consumers.

Option C: execute the capability directly from OperationalSession. Reject:
bypasses planning, worker/queue lifecycle and pipeline evidence.

## Acceptance and non-goals

If approved, one separate implementation work order may change session,
Executive manager/orchestrator/pipeline, factory wiring as needed, PlannerManager
and focused tests. It must prove the real public-session path creates one
print-only source file, returns execution evidence and completes its canonical
Objective; invalid input/ownership/disabled submission writes no execution
state; failure/recovery remain truthful; repeat submission cannot replace Plans;
ordinary behavior, isolated workspaces and active data remain unchanged.

Full tests, compile/import checks and architecture review are required. No CLI,
Content OS, new model/provider, shell/Git operation, migration, concurrent-writer
guarantee, autonomous retry or relaxation of the print-only fixture.

## Decision request

Approve, revise or reject **Option A: explicit session intent submission through
the existing Executive pipeline**, including its direct-to-Executive boundary.
This proposal does not authorize implementation until selected by the owner.

No tests rerun for this documentation-only assessment; WO-117's 213-test
baseline remains the latest executable evidence. Unrelated edits are untouched.
