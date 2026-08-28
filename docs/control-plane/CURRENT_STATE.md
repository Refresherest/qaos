# QAOS Current State

**Recorded:** 2026-08-29 UTC

**WO-068 base:** `ef0b703` (`feat/operational-builder-chain`)

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
- WO-044 implements Option A: Kernel validates a canonical Objective, resolves
  the explicit Runtime executive, returns its result, and performs no implicit
  persistence. FINDING-017 is resolved.
- WO-045 resolves FINDING-018: ExecutionEngine accepts explicit planner and
  queue collaborators while preserving execution order and default behavior.
- WO-046 resolves FINDING-019: ExecutionManager accepts an explicit engine
  registry and ObjectiveManager while preserving execution-before-save order.
- WO-047 resolves FINDING-020: LearningManager, Learner, and LearningEngine form
  an explicit chain to isolated memory and knowledge managers.
- WO-047 recorded FINDING-021 as an unrelated reloaded-reflection identity
  mismatch in Learner; the live canonical Objective path was unaffected.
- WO-048 resolves FINDING-021 by applying LearningEngine's established
  Objective-or-string identity normalization in Learner without rehydration.
- WO-049 resolves FINDING-022: PlannerManager, PlanGenerator, ContextManager,
  RetrievalManager, and RetrievalEngine now retain caller-selected workspace
  services through the complete planning chain.
- WO-050 resolves FINDING-023: ClassifierManager now retains a caller-selected
  IntentClassifier-compatible service while preserving its default ruleset.
- WO-051 resolves FINDING-024: CouncilManager and Delegator now retain selected
  council, objective, and queue ownership through an instantiable registry.
- WO-052 resolves FINDING-025: QueueManager now retains a caller-selected worker
  service while preserving default worker resolution and queue persistence.
- WO-053 resolves FINDING-026: WorkerManager, DefaultWorker, and AgentManager now
  retain caller-selected worker and agent ownership through isolated registries.
- WO-054 resolves FINDING-027: Agent, SkillResolver, and SkillManager now retain
  caller-selected skill ownership through an isolated SkillRegistry.
- WO-055 resolves FINDING-028: Skill and CapabilityManager now retain
  caller-selected capability ownership through an isolated CapabilityRegistry.
- FINDING-029 records that the built-in `system` capability exists but is not
  registered in the default lifecycle; WO-055 does not choose that lifecycle.
- WO-056 resolves FINDING-029 by applying the established built-in package
  registration pattern to the canonical `system_capability`; the complete
  default Agent-to-Skill-to-Capability path passes in a clean process.
- WO-057 resolves FINDING-030: DefaultWorker now completes successful QueueItem
  lifecycle state, timestamps, and result while preserving delegated outputs.
- WO-058 proves one fully explicit Kernel-to-Capability runtime using isolated
  Stores: classification, delegation, five planned tasks, six QueueItems,
  reflection, and learning all complete without active-data writes.
- FINDING-031 records that the successful ExecutionResult and completed queue
  coexist with a canonical Objective that remains `pending`.
- WO-059 resolves FINDING-031 by assigning start/complete/fail lifecycle ownership
  to ExecutionManager, the existing boundary that owns ObjectiveManager.
- WO-060 records DECISION-REQUEST-004: the verified explicit runtime has no
  authorized production composition root. Option A, an Executive composition
  factory, is recommended; no product code changed.
- OWNER-DECISION-004 selects Option A. WO-061 implements the public,
  provider-neutral `create_executive` factory with isolated registries and an
  optional shared ObjectiveManager for coherent lifecycle persistence.
- WO-062 records DECISION-REQUEST-005 for the first application-facing
  consumer. Option A, an operational application session above Executive and
  Kernel, is recommended; no product code changed.
- OWNER-DECISION-005 selects Option A. WO-063 implements
  `qaos.application.OperationalSession`, which owns one explicit workspace and
  shared objective lifecycle while preserving Kernel and Executive contracts.
- WO-064 records DECISION-REQUEST-006 for the first adapter over
  OperationalSession. Option A, a one-shot CLI objective operation requiring
  an explicit workspace, is recommended; no product code changed.
- OWNER-DECISION-006 selects Option A. WO-065 implements the one-shot
  `objective --workspace <path> <goal...>` CLI adapter with deterministic 0/1/2
  process statuses and no implicit active-data target.
- WO-066 manually verifies that adapter against a fresh disposable workspace:
  exit 0, one completed objective, five completed tasks, six completed queue
  items, and persisted reflection, memory, and knowledge evidence. Active data
  remained unchanged and the disposable workspace was removed.
- FINDING-032 records that an unmatched goal reports `Classification: None`
  while continuing successfully; the desired policy requires an owner decision.
- WO-067 records DECISION-REQUEST-007 with three policies for FINDING-032.
  Option B, canonical `general_objective` fallback with continued execution, is
  recommended; no product code changed.
- OWNER-DECISION-007 selects Option B. WO-068 configures the canonical default
  classifier with `general_objective` fallback after explicit rules miss while
  preserving custom classifier control. FINDING-032 is resolved.
- Current verification passes 106 tests. The architecture inspector no longer
  reports `ENTITY-OBJECTIVE-SELF-PERSISTENCE`; unrelated findings remain. See
  VERIFICATION-061.

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
2. Select the next QAOS operational-readiness gap through a separate
   evidence-led work order; do not infer classification-driven routing.
3. Do not infer production-provider readiness or expand into publishing, UI,
   retries, or other excluded features from this test-only slice.
4. Address any newly prioritized architecture finding only through its own
   evidence-backed work order.
5. Do not infer CLI or raw-goal authorization from WO-044; those remain separate
   future decisions.
