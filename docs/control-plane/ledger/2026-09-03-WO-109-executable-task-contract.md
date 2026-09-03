# WO-109 — Executable Task Contract Proposal

Baseline: 4d09a1a on feat/operational-builder-chain, 2026-09-03.

Objective: define options and acceptance criteria for one deterministic task
that produces and verifies source in a disposable workspace. Scope is analysis
and owner decision request only. No product code, schema, provider, credentials,
deployment, shell autonomy, Git behavior or Content OS expansion.

Evidence inspected: Task, QueueItem, Agent, Capability, SystemCapability,
Artifact, planner generator, executive factory, WO-108, and current authority.
Stop after recording a bounded recommendation.

## Architectural question

Where should explicit executable intent live while preserving current identity,
queue and recovery ownership?

### Option A — Task-owned typed intent (recommended)

Add an optional, provider-neutral, serializable intent to `Task`. The first and
only allowed type would describe writing one UTF-8 source file beneath an
explicit workspace and verifying it with one allowlisted Python invocation.
QueueItem continues to reference/carry the Task; a specifically registered
capability validates and executes the intent. Existing description-only and
legacy Tasks retain current behavior.

Consequence: intent stays with the durable unit of planned work and therefore
participates in existing Task identity, Plan persistence, failure, and recovery.
This extends an existing concept rather than creating another workflow system.

### Option B — QueueItem-owned intent

Store executable detail on QueueItem only. This localizes worker input but
separates durable task meaning from the Plan and duplicates state that recovery
must reconcile. Not recommended.

### Option C — Infer execution from Task.description

Parse human-readable descriptions into operations. This avoids a field but is
ambiguous, hard to validate, and unsafe as an authorization boundary. Reject.

## Proposed first acceptance contract

If Option A is approved, a separate implementation work order will prove only:

1. The caller supplies an explicit disposable workspace and one validated typed
   intent containing a relative `.py` path and complete UTF-8 source content.
2. Resolution rejects absolute paths, traversal, symlinks escaping the
   workspace, pre-existing target files, non-`.py` targets, blank/oversized
   content, unknown intent versions/types, and unapproved verification forms.
3. Execution writes exactly one source file atomically beneath the workspace.
4. Verification invokes the current Python interpreter directly—never a shell—
   with that exact file, a timeout, captured stdout/stderr, and no user-provided
   flags, environment substitutions, network operation, package installation,
   Git command, deletion, or external path.
5. Acceptance succeeds only when exit code is zero and stdout equals an exact
   expected string from the intent. The QueueItem and Task complete only then.
6. Write or verification failure makes Task, QueueItem, and Objective truthfully
   failed through existing lifecycle ownership; raw private error payloads are
   not exposed by the CLI.
7. Execution evidence records intent type/version, relative path, source digest,
   verifier identity, exit code and bounded captured output. Credentials and
   absolute host paths are excluded.
8. Re-execution never overwrites a target. Recovery after a file was written but
   verification failed must stop with an explicit conflict; exactly-once side
   effects are not claimed.
9. Existing description-only Tasks, Content OS, recovery semantics, CLI syntax,
   active data, default provider selection, and model governance remain unchanged.
10. Tests use only disposable workspaces and demonstrate zero active-data writes.

The first fixture should be deliberately tiny: generate one Python program that
prints one predetermined line, then verify that exact output. Passing proves a
real bounded build action and evidence path—not general autonomous app building,
production safety, arbitrary code authorization, or model quality.

## Decision request

Owner: approve, revise, or reject **Option A: Task-owned typed intent** and the
ten acceptance rules above. Approval authorizes a separate implementation work
order; it does not authorize implementation in WO-109.

No tests were required or run because this work order changes control-plane
documents only. All unrelated working-tree changes remain untouched.
