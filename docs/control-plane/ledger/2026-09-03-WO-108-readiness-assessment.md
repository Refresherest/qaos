# WO-108 — Operational Readiness Assessment

Owner authorization: proceed after HANDOFF-098. Baseline: 6cda2d3 on
feat/operational-builder-chain; Python 3.14.3, 2026-09-03.

Objective: compare the proven local runtime with the approved purpose of QAOS
building downstream applications. Scope: read source, approved decisions,
tests and control-plane evidence; record assessment only. No implementation,
provider calls, deployment, credential changes or draft-ADR promotion.

Verification: architecture inspector, full regression suite, source inspection
of executive factory, planner generator, SystemCapability, worker, JSONStore
and Content OS first slice. Stop after documenting one recommended next step.
Recovery: documentation-only; no runtime migration or rollback needed.

## Assessment

| Area | Evidence | Readiness boundary |
| --- | --- | --- |
| Local orchestration | OperationalSession, explicit executive factory, WO-107 rehearsal | Identified local work can fail, reload, be discovered and explicitly recovered. |
| Actual app building | planner/generator.py creates fixed task descriptions; capabilities/system.py explicitly reserves actual LLM/tool execution for later | Completing these tasks proves lifecycle transitions, not implementation or validation of software. This is the primary product gap. |
| Content OS | content_os/first_slice.py generates an artifact through an injected test-only provider and reviewer | A bounded separate consumer, not proof that the generic executive builds apps. Production providers remain excluded by OWNER-DECISION-001/002. |
| Side-effect safety | executive/factory.py registers SystemCapability only; filesystem.py accepts supplied paths; git.py uses ambient working directory | Existing utility classes are not evidence of an authorized, workspace-confined builder. Do not wire them into autonomous execution without a contract. |
| Durable recovery | JSONStore atomically replaces individual files; explicit recovery checks related records | Caught failures are tested. Multi-file transactions, concurrent writers, abrupt process death and exactly-once external side effects are not established by that proof. |
| Cloud builders | WO-018 and current state | Last recorded OpenHands startup blocker remains; no fresh Cloud check in this assessment. It does not prevent local work. |

The architecture inspector reviewed 188 Python files. Its duplicate-class,
registry and singleton findings remain review leads, not authority to refactor:
its cited draft ADRs cannot override AUTHORITY_AND_RECONCILIATION.md.

## Recommended next work package

Define an acceptance contract for ONE deterministic app-building task in an
explicit disposable workspace: approved input, one generated source artifact,
a bounded verification command, captured result and truthful failed/completed
status. Specify allowed paths, forbidden operations and repeated-execution
behavior before implementation. Reuse existing Task, Queue, Capability and
Artifact concepts; do not introduce a parallel orchestration system.

This is a proposal, not an approved design. First settle how executable intent
and acceptance evidence attach to existing tasks. Start with a deterministic
test implementation; production model choice, shell autonomy, Git writes,
publishing, UI, GPU and general autonomous app building remain out of scope.

This addresses the largest capability gap without waiting for OpenHands or
claiming that every future platform feature must be complete first.

## Verification result and handoff

PASS: `.venv\Scripts\python.exe -m pytest -q -p no:cacheprovider --basetemp C:/Projects/qaos/.wo108-test-tmp`
reported 182 passed in 21.10s. Architecture inspection command:
`.venv\Scripts\python.exe tools/architecture_inspect.py` (188 files).
No new compile/import sweep or live provider/Cloud probe was performed.
No product code changed. Pre-existing skill edits, draft documents and tooling
remain untouched; the test scratch directory is local and excluded from scope.

Assessment complete. Next: owner-authorized executable-task acceptance-contract
proposal, not implementation. Read this record, CURRENT_STATE.md,
AUTHORITY_AND_RECONCILIATION.md and OWNER-DECISION-001/002 first.
