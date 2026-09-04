# WO-130 — Trusted Multi-File Project Proposal

2026-09-04; baseline b89576a, feat/operational-builder-chain.
Authority: owner requested the proposal following HANDOFF-109.
Objective: define one bounded project-output contract, compare alternatives and
request approval. Scope: proposal/current-state/handoff only. No product code,
execution permission, provider, credentials or active-data changes. Stop after
recording the proposal and requesting owner decision.

## Evidence

WO-128/129 establish trusted single-file CLI generation and fresh-process use,
discovery, no-overwrite refusal and per-template recovery authorization. The
253-test baseline is VERIFICATION-109, not rerun for this proposal.
src/qaos/capabilities/python_file.py atomically creates one file through a hard
link, then verifies it. That implementation does not define publication of a
directory, multiple-file ownership, or recovery after partial project output.
Existing identity/path-only template selection and Task/Plan/Queue lifecycle
remain useful; a new output shape must not silently change their old contracts.

## Option A — One staged, verified trusted project (recommended)

Propose template `text_stats_project_v1` producing exactly four files:

- stats.py: pure text_stats function, same OWNER-DECISION-025 semantics.
- app.py: imports stats and exposes OWNER-DECISION-026's CLI contract.
- test_stats.py: fixed standard-library acceptance tests for cross-file behavior.
- README.md: invocation, limits, non-sensitive argument warning and template ID.

One project is one Task within the existing PlannerManager-owned Plan, not one
Task per file. No new workflow engine. Source/test/documentation bytes are
repository-owned. No caller filenames, code, dependencies or commands.

Use a new versioned `python_project` intent carrying only template ID and a
relative project-directory name. For this first version, allow a single ASCII
directory component matching [A-Za-z][A-Za-z0-9_-]{0,63}, excluding Windows
reserved device names case-insensitively. No nested paths, dot names, separators,
drive prefixes or caller-selected member paths. Unknown fields/types/versions fail.
Introduce separate empty-default `enabled_python_projects` permission plus an
explicit existing absolute `python_project_workspace` output root on factory
and session. Existing file/template opt-ins grant no project authority.

### Ownership and publication

1. Never write into an existing destination, even an empty directory or matching
   old output. Refuse files, links and reparse-point destinations as well.
2. Create a uniquely owned private staging directory under the selected output
   root, on the same filesystem as its final destination. Populate only the four
   fixed files; no user data is moved or adopted.
3. Verify exact bytes and fixed member set, cross-file tests and independent CLI
   cases before publication. Suppress bytecode output; reject unexpected members.
4. Publish the verified directory with one no-replace directory operation. A
   check-then-overwriting rename is not acceptable. The supported filesystem/OS
   primitive must first pass a bounded evidence gate proving collision refusal,
   including an empty destination and a competing publisher. If unavailable or
   unproven, stop: do not substitute merge/copy or weaken the contract silently.
5. Verify the final member set/digests read-only, then complete the Task. Record
   template/version, project-relative path, sorted member SHA256 digests and
   verifier outcome in existing execution evidence. No absolute paths or secrets.

Atomic publication means visibility of one verified directory transition; it is
not a claim of transactional coupling with JSON execution state, power-loss
durability, or safety against a hostile process modifying the output filesystem.
Supported platform scope must be explicit in implementation evidence; no inferred
cross-platform or network-filesystem guarantee.

### Failure and recovery

- Ordinary pre-publication failure: no final project; mark execution failed and
  clean only the current attempt's known staging directory after confirming its
  resolved path and ownership remain confined. Never clean by broad wildcard.
- If cleanup itself fails, report the residual stage separately, preserve it and
  fail; do not hide the error or mark complete.
- Crash before publication may leave a stage. Never scan/delete/adopt abandoned
  stages automatically. Record this limitation; owner-directed cleanup is separate.
- Collision at publication: preserve the existing destination byte-for-byte;
  discard only the current owned stage where safe and retain failed lifecycle.
- Crash/failure after publication but before state completion can leave a complete
  project alongside incomplete/failed state. Explicit recovery must refuse the
  existing destination, even if hashes match; no automatic adoption or overwrite.
  Report the discrepancy for owner-directed reconciliation, without claiming a
  rollback of the published project or success that was not recorded.
- Recovery requires the same project permission. If the destination is absent,
  explicit recovery may rerun the fixed template in a new stage through existing
  recovery semantics. No automatic retry, stage reuse or resume-in-place.

### Verification gate

Before implementation acceptance require: publication primitive tests on the
declared platform; public-session success with all four exact members; standalone
cross-file import/CLI behavior; corrupted/missing/extra member rejection;
fault injection before publication and after publication before completion;
concurrent target collision; unauthorized submission/reload without state writes;
safe cleanup and cleanup-failure evidence; unchanged existing destination hashes;
full regressions, compile checks, fresh-process rehearsal and unchanged active data.
Acceptance includes independent literal expectations, not only generated tests
or a success marker. Use fixed shell=False commands, bounded per-process timeouts
and bounded evidence. This does not authorize a general command runner.

## Alternatives

Option B: create files directly in an exclusively claimed final directory, with
a completion marker written last. Simpler publication mechanism, but partial
projects remain externally visible and consumers must obey a new marker contract.
Not equivalent to Option A; would require separate approval of that tradeoff.

Option C: remain single-file. Lowest scope/risk, but does not test project
structure or cross-file assembly. Valid if project-publication scope is premature.

## Owner decision requested

Approve, revise or reject Option A, including its prerequisite primitive gate
and refusal-based recovery after a publish/state gap. Approval authorizes a
separate bounded implementation work order, not immediate product changes here.
No models, arbitrary code, installs, Git capability, UI, QAOS CLI changes,
external publishing or Content OS feature expansion. Local filesystem publication
in this proposal does not mean deployment to an external service.

Architecture-awareness identified the new ownership/publication boundary and
kept it explicit rather than widening python_template v1. No runtime tests or
platform guarantees established in this documentation-only work order. JSON and
whitespace checks verify records only. Unrelated modified skills and untracked
configuration/drafts/test directories preserved. Rollback: revise/remove only
these proposal records with owner direction; no migration.
