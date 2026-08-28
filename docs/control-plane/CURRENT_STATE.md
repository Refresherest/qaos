# QAOS Current State

**Recorded:** 2026-08-28 UTC

**WO-043 base:** `eaff473` (`feat/operational-builder-chain`)

**Core baseline:** `615cbbb` (`main`)
**Status:** Core recovery and reproduced MemoryManager storage isolation are
verified; Builder Chain named-profile validation is blocked before delegation
by OpenHands Cloud parent-runtime startup.

## Verified Core State

- WO-001 through WO-008 recovered explicit core construction, deterministic
  pipeline stage ownership, CLI/kernel routing, retired duplicate runtime
  paths, and fail-safe active JSON storage.
- WO-009 characterized active storage construction and obtained owner approval
  for the proposed explicit boundary.
- WO-010 implemented `create_stores(data_dir) -> Stores`, moved the seven
  active domain managers to explicit storage collections, removed the dead
  planner storage path, and preserved JSON semantics.
- `ec2e879` committed the explicit storage boundary to `main`.
- WO-020 resolves FINDING-003 for MemoryManager: explicit stores receive private
  registry state by default, the default module manager retains compatibility,
  and active persisted data is verified unchanged.
- OWNER-DECISION-001 accepts the Content OS boundary, first slice, exclusions,
  readiness-first dependency order, and review vocabulary.
- WO-022 verifies the same private-registry contract for explicitly stored
  ArtifactManagers without changing default compatibility behavior.
- WO-023 verifies the same private-registry contract for explicitly stored
  ObjectiveManagers without changing default compatibility behavior or the
  Objective entity self-persistence contract.
- WO-024 verifies private registry state for explicitly stored PlannerManagers.
  Memory, Artifact, Objective, and Plan workspace isolation now satisfy Content
  OS readiness Gate 2.
- WO-025 adds explicitly injected, provider-neutral AI generation with immutable
  prompt/output evidence without mutating global provider selection. This
  satisfies Content OS readiness Gate 3.
- WO-026 records CONTRADICTION-002: Gate 4 requires Content OS-specific brief
  validation and review behavior, while OWNER-DECISION-001 requires Gate 4 to
  pass before Content OS implementation. No product code was changed.
- OWNER-DECISION-002 approves Option A and resolves CONTRADICTION-002. Gates
  1–3 remain prerequisites; Gates 4–5 are mandatory acceptance criteria of the
  separately scoped first Content OS slice.
- WO-028 implements the bounded `Brief -> Reviewed Draft Artifact` slice in a
  separate `content_os` package. Success, invalid-brief, provider-failure,
  review-outcome, isolation, and test-provider governance behavior are proven.
- WO-029 resolves FINDING-004: the built-in MockProvider is explicitly named
  `mock`, matching default configuration and AIEngine selection.
- WO-030 resolves FINDING-005: ArtifactManager resolves canonical string titles
  immediately and after persistence reload, preserving entity-object lookup.
- WO-031 resolves FINDING-006: MemoryManager resolves and unregisters canonical
  string titles immediately and after persistence reload.
- WO-032 resolves FINDING-007 by retiring the dead, duplicate, unimportable
  `qaos.queue.queue_db` module. The full 180-module QAOS import sweep now passes
  without exclusions.
- WO-033 resolves FINDING-008: Objective transitions are state-only, while the
  explicitly selected ObjectiveManager owns persistence. Council uses the
  default manager explicitly and Content OS uses its isolated manager.
- WO-034 resolves FINDING-009: explicitly stored QueueManagers now own private
  registry state, while the default manager and compatibility functions retain
  the default registry.
- WO-035 resolves FINDING-010: explicitly stored KnowledgeManagers now own
  private registry state, preventing cross-workspace lookup and persistence.
- WO-036 resolves FINDING-011: explicitly stored ReflectionManagers now own
  private registry state while objective/string identity behavior remains.
- WO-037 resolves FINDING-012: explicitly configured event managers and buses
  can own isolated subscriber state while default Council behavior remains.
- WO-038 resolves FINDING-013: ExecutivePipeline accepts explicit dependencies
  for all six stages while preserving its default manager composition.
- WO-039 resolves FINDING-014: an explicit pipeline can now flow through an
  explicit ExecutiveOrchestrator and ExecutiveManager, including logging.
- WO-040 resolves FINDING-015: Runtime and Kernel can retain an explicitly
  composed executive service without importing a default singleton.
- WO-041 resolves FINDING-016: Dispatcher and Kernel accept isolated command
  surfaces while preserving every default CLI command and result contract.
- WO-042 records FINDING-017 and DECISION-REQUEST-003: the first executive
  invocation boundary requires an owner choice and no product code changed.
- OWNER-DECISION-003 selects Option A: a programmatic
  `Kernel.execute_objective(objective)` boundary. WO-043 records this decision;
  implementation remains a separate work order.
- Current verification passes 57 tests. The architecture inspector no longer
  reports `ENTITY-OBJECTIVE-SELF-PERSISTENCE`; unrelated findings remain. See
  VERIFICATION-035.

## Verified Builder Chain State

- WO-014 introduced six OpenHands file-based agents and the bounded
  CSA -> PE -> Reviewer protocol.
- SMOKE-001 completed the three-stage sequence using `model: inherit`. This
  proves agent discovery, sequential orchestration, package handoffs, and
  Reviewer acceptance under the parent conversation model only.
- WO-018 binds both agents at each stage to the matching `QAOS_CSA`, `QAOS_PE`,
  or `QAOS_REVIEWER` profile.
- SMOKE-002 has not reached agent discovery or named-profile resolution. Two
  fresh no-repository conversations failed after prompt submission with
  `Error occurred` and `Waiting for runtime to start...`.
- The published role-profile mapping remains in place because the restoration
  condition—delegated named-profile resolution failure—has not occurred.

## Evidence Boundaries

- `VERIFIED`, `VALIDATED`, and `DESIGNATED` remain independent model-governance
  states.
- OpenHands and OmniRoute are integrations, not QAOS architectural authority.
- The existing untracked `docs/architecture/` and `docs/vision/` material
  remains draft evidence only unless reconciled through an owner-approved
  decision.
- Pre-existing unrelated modified and untracked working-tree files remain
  outside the Builder Chain and current-state reconciliation scopes.

## Product Direction

The owner accepted PROPOSAL-004 through OWNER-DECISION-001 and revised its
sequencing through OWNER-DECISION-002. The `Brief -> Reviewed Draft Artifact`
first slice is implemented and verified. Gates 1–5 pass. External publishing,
production providers, UI, retries, and later Content OS features remain
excluded. `ACCEPT`, `REVISE`, and `BLOCKED` remain the review terms for this
slice.

## Open Priorities

1. Obtain OpenHands platform evidence for the parent-runtime startup failure;
   do not change QAOS profiles or product code in response to that failure.
2. Review the verified first-slice evidence and choose the next bounded QAOS or
   Content OS increment through a new owner-authorized work order.
3. Do not infer production-provider readiness or expand into publishing, UI,
   retries, or other excluded features from this test-only slice.
4. Address any newly prioritized architecture finding only through its own
   evidence-backed work order.
5. Issue one bounded work order implementing OWNER-DECISION-003 Option A. Do not
   add a CLI command, create Objectives implicitly, or repurpose `run`.
