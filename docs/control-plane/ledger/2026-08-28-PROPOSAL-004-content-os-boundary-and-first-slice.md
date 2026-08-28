# PROPOSAL-004 — Content OS Boundary and First Validation Slice

## Authority State

`ACCEPTED — OWNER-DECISION-001`

The owner accepted all five requested decisions on 2026-08-28. This document
now governs the first-slice boundary and dependency order. Content OS
implementation remains gated by the approved QAOS readiness work.

## Owner-Stated Direction

- QAOS's purpose includes building downstream applications.
- Content OS is intended to be the first downstream application.
- QAOS should reach a reliable operational foundation before Content OS depends
  on it, while Content OS should eventually provide a real consumer test of
  QAOS rather than waiting for an abstract claim of total platform completion.

## Verified QAOS Capabilities Available Today

- Explicit `create_runtime(configuration, ...)` construction.
- A six-stage executive sequence: classify, delegate, plan, execute, reflect,
  and learn.
- Objective, execution-report, and artifact domain objects.
- Explicit `create_stores(data_dir) -> Stores` construction.
- Verified private MemoryManager registry state for explicitly stored managers.
- A provider-neutral `AIProvider.generate(prompt)` interface with a mock
  provider.
- Twenty-one passing regression tests, including deterministic pipeline stage
  ownership and focused storage-boundary tests.

## Current Limitations Relevant to Content OS

- The executive pipeline is stage-tested with substituted managers, not proven
  as a real brief-to-artifact integration path.
- The current AI engine uses a global active-provider name and only the mock
  provider is tracked as built-in evidence.
- A canonical, governed model-resolution path is not demonstrated in the
  current tracked source tree.
- ArtifactManager has an explicit store parameter but its registry lifecycle
  has not received the isolation proof completed for MemoryManager.
- Error recovery, retry semantics, and resumability for a downstream product
  workload are not yet characterized.
- OpenHands Builder Chain named-profile validation remains blocked before
  delegation; this does not block local QAOS architecture work.

## Proposed Source-of-Truth Boundary

### QAOS owns generic operating-system concerns

- Objective and task orchestration
- Workflow execution and status
- Provider-neutral model identity, governance, and resolution
- Generic artifact infrastructure and persistence
- Memory, knowledge, events, reflection, and learning infrastructure
- Capability authorization, audit evidence, and failure semantics
- Runtime construction and dependency injection

### Content OS would own content-domain concerns

- Content briefs and their domain validation
- Audience, message, voice, and brand-context inputs
- Content-type and channel requirements
- Editorial stages and content-specific review criteria
- Content revisions and approved content versions
- Content calendars, campaigns, publishing, and performance interpretation
  only when separately authorized in later slices

### Boundary rule

Content OS may translate a content brief into QAOS objectives and consume QAOS
artifacts and execution evidence. It must not become the canonical source for
QAOS models, providers, generic tasks, runtime state, or governance.

## Proposed First Vertical Slice

### Name

`Brief -> Reviewed Draft Artifact`

### Input

A small structured brief containing:

- working title
- purpose
- intended audience
- core message
- requested content type
- constraints supplied as plain text

### Flow

1. Content OS validates the brief.
2. Content OS translates it into one QAOS objective.
3. QAOS plans and executes one deterministic draft-generation task through an
   injected test provider.
4. QAOS stores one generic artifact containing the draft and provenance.
5. A bounded review step returns `ACCEPT`, `REVISE`, or `BLOCKED` with reasons.
6. The caller receives objective status, artifact identity, review result, and
   execution evidence.

### Explicit exclusions from the first slice

- External publishing or social-platform access
- Editorial calendar and campaign management
- Analytics, SEO scoring, or performance feedback
- Multiple content formats in one objective
- Autonomous retries or open-ended agent loops
- Production provider selection or model designation
- UI/dashboard work
- GPU workloads

## QAOS Readiness Gates Before Slice Implementation

### Gate 1 — Reproducible core baseline

- Full regression suite passes from a documented command and writable temp
  root.
- Compile and package-import checks pass.
- Active persisted data remains unchanged during isolated tests.

**Current state:** passed for the 21-test baseline.

### Gate 2 — Isolated objective-to-artifact workspace

- The managers required by the slice accept one explicit `Stores` collection.
- Two slice executions using different data directories cannot observe or
  persist each other's objectives, plans, artifacts, or memories.

**Current state:** not proven. Memory isolation alone is insufficient.

### Gate 3 — Deterministic generation contract

- The slice can inject a deterministic provider without changing global model
  or provider state.
- Prompt/request input and generated output are captured as execution evidence.

**Current state:** not proven by tracked tests.

### Gate 4 — End-to-end status and failure contract

- Success produces exactly one reviewed artifact and completed objective.
- Invalid briefs fail before model execution.
- Provider failure produces a recorded failed or blocked result without a
  partial approved artifact.

**Current state:** not proven.

### Gate 5 — Governance boundary

- The test provider is explicitly test-only.
- Availability or successful generation does not imply model `VALIDATED` or
  `DESIGNATED` status.
- No credential values enter source control or execution evidence.

**Current state:** governing rule exists; slice-specific proof is pending.

## Recommended Dependency Order

1. Owner accepts or revises this boundary and first-slice definition.
2. CSA issues one QAOS-readiness work order for Gates 2–5; no Content OS domain
   implementation in that work order.
3. Reviewer verifies the readiness gate.
4. CSA issues a separate first-slice implementation work order.
5. Implement and test the slice against isolated stores and a deterministic
   provider.
6. Use the slice evidence to decide the next QAOS or Content OS increment.

## Owner Decisions Requested

Approve, revise, or reject each item independently:

1. **Product boundary:** Content OS owns content-domain concepts while QAOS
   owns generic orchestration, model governance, runtime, and artifact
   infrastructure.
2. **First slice:** `Brief -> Reviewed Draft Artifact` is the first integration
   target.
3. **No publishing:** External publishing and channel credentials are excluded
   from the first slice.
4. **Readiness first:** Gates 2–5 must pass before Content OS implementation.
5. **Review vocabulary:** The first slice uses `ACCEPT`, `REVISE`, and
   `BLOCKED` as content-review outcomes.

## Recommendation

Approve items 1–4. Item 5 should be confirmed against the owner's preferred
design and editorial language before it becomes a domain contract.

## Owner Disposition

All five items were approved. The `ACCEPT`, `REVISE`, and `BLOCKED` vocabulary
is accepted for now and may be revised later through a new recorded decision.
See OWNER-DECISION-001.
