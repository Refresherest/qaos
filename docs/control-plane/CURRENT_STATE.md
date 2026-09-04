# QAOS Current State

**Recorded:** 2026-09-04 UTC

**WO-140 base:** `7d25f87` (`feat/operational-builder-chain`)

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
- WO-069 verifies that fallback through the real one-shot CLI: an unmatched
  goal reports `general_objective`, exits 0, and persists one completed
  objective, five completed tasks, six completed queue items, reflection,
  memory, and knowledge in a disposable workspace. Active data is unchanged.
- WO-070 reproduces FINDING-033: a failure before ExecutionManager starts leaves
  the application-created Objective persisted as pending even though execution
  fails. Lifecycle ownership requires an owner decision; no code changed.
- WO-071 records DECISION-REQUEST-008 with three ownership options for
  FINDING-033. Option A, an OperationalSession-owned conditional pending-to-fail
  transition, is recommended; no product code changed.
- OWNER-DECISION-008 selects Option A. WO-072 makes OperationalSession fail and
  persist only a still-pending Objective when Kernel raises, preserves the
  original exception, and leaves downstream transitions untouched.
  FINDING-033 is resolved.
- WO-073 reproduces FINDING-034: a delegated DefaultWorker exception leaves the
  live QueueItem `running`, while its persisted and reloaded form remains
  `pending`; the Task also remains `pending`. Queue-item failure lifecycle and
  durable persistence ownership require an owner decision. No code changed.
- OWNER-DECISION-009 selects Option A. WO-074 makes DefaultWorker fail its
  running QueueItem on delegated failure, conditionally fails only a Task that
  actually started, preserves the original exception, and makes QueueManager
  persist state before the exception escapes. FINDING-034 is resolved.
- WO-075 characterizes FINDING-035: in a three-item queue, failure of the
  second item persists the batch as `completed, failed, pending`; the third
  item is not attempted. This state is internally consistent, but QAOS has no
  designated partial-plan disposition policy. No code changed.
- OWNER-DECISION-010 selects Option A. WO-076 designates and regression-tests
  the existing fail-fast processing boundary: stop at the first failure,
  persist `completed, failed, pending`, preserve the original exception, and
  leave continuation to a separately authorized recovery operation.
  FINDING-035 is resolved without product-code changes.
- WO-077 reproduces FINDING-036: after fail-fast state
  `completed, failed, pending`, a second ordinary QueueManager processing call
  silently executes the pending remainder and persists
  `completed, failed, completed`. QAOS has no attempt identity or authorized
  recovery boundary governing that continuation. No code changed.
- OWNER-DECISION-011 selects Option A. WO-078 records that ordinary queue
  processing is not an authorized recovery mechanism and that a canonical
  execution-attempt identity plus explicit recovery boundary must be designed
  before enforcement. Objective, Plan, QueueItem, schemas, and product code
  remain unchanged; FINDING-036 stays open pending that design.
- WO-079 completes the bounded identity design assessment. Existing Objective
  lifecycle already represents one operational invocation closely enough that
  a separate ExecutionAttempt aggregate would duplicate state. PROPOSAL-005
  recommends canonical opaque Objective identity as the attempt identity,
  propagated by reference to Plan and QueueItem with legacy records remaining
  unassigned and non-recoverable. No code or schema changed.
- OWNER-DECISION-012 selects Option A. WO-080 designates immutable opaque
  Objective identity as the canonical execution-attempt identity, with Plan
  and QueueItem as downstream references only. Goal text remains compatibility
  and display data. FINDING-036 stays open pending ID-generation, registry,
  persistence, and propagation contracts. No code or schema changed.
- WO-081 completes the Objective identity contract assessment. PROPOSAL-006
  recommends ObjectiveManager-injected opaque IDs, a canonical ID index plus a
  latest-by-goal compatibility projection, and pass-through loading of legacy
  unidentified records without migration inference. No code or schema changed.
- OWNER-DECISION-013 selects Option A. WO-082 records manager-injected opaque
  Objective IDs, canonical ID plus latest-by-goal registry indexes, and truthful
  pass-through of unidentified legacy records. Duplicate IDs fail closed; the
  exact error type remains a bounded implementation detail. No code or schema
  changed.
- WO-083 implements the bounded Objective identity foundation. ObjectiveManager
  assigns injectable opaque IDs to new Objectives; ObjectiveRegistry preserves
  canonical ID lookup, latest-by-goal compatibility, and complete equal-goal
  records; legacy missing-ID records remain unidentified; duplicate IDs fail
  closed. Plan, QueueItem, migration, and recovery remain unchanged.
- WO-084 completes the bounded Plan and QueueItem propagation assessment.
  PROPOSAL-007 recommends additive non-owning `objective_id` references, a dual
  PlanRegistry with complete-record persistence, and QueueItem pass-through
  without uniqueness or recovery semantics. No product code or schema changed.
- OWNER-DECISION-014 selects Option A. WO-085 records additive non-owning
  Objective ID references for Plan and QueueItem, dual Plan indexes, complete
  Plan persistence, and legacy missing-reference pass-through. Migration and
  recovery remain excluded. No product code or schema changed.
- WO-086 implements Objective-ID propagation through Plan, PlanRegistry,
  PlannerManager, QueueItem, QueueManager, CouncilManager, and ExecutionEngine.
  Equal-goal Plans remain complete and identity-addressable, multiple QueueItems
  share one reference, and legacy missing-reference records remain unchanged.
  Migration and recovery behavior remain excluded.
- WO-087 completes the explicit recovery assessment. PROPOSAL-008 recommends
  attempt-scoped retry from the failed item through its pending remainder,
  ExecutionManager lifecycle ownership, and an ordinary-processing guard that
  skips only failed identified attempts while permitting unrelated work. No
  product code or schema changed.
- OWNER-DECISION-015 selects Option A. WO-088 records explicit Objective-ID
  recovery that retries the failed item then its pending remainder, preserves
  completed and unrelated work, and prevents ordinary processing from silently
  continuing failed identified attempts. No product code or schema changed.
- WO-089 confirms FINDING-037: after reload, a Plan Task and its QueueItem action
  are separate objects with no canonical Task identity. Resetting the queue copy
  leaves the Plan copy failed, so durable coherent recovery cannot implement
  OWNER-DECISION-015 safely. PROPOSAL-009 recommends PlannerManager-assigned
  opaque Task identity and explicit QueueItem task references. No product code
  or schema changed.
- OWNER-DECISION-016 selects Option A. WO-090 records PlannerManager-assigned
  immutable opaque Task IDs, explicit Plan Task lookup, and non-owning QueueItem
  action references with truthful legacy omission. Recovery remains blocked
  until this foundation is implemented and verified. No product code changed.
- WO-091 implements the Task identity foundation. PlannerManager assigns opaque
  IDs to new Tasks before queueing or persistence, Plan provides explicit Task
  lookup, QueueItem carries a validated non-owning action reference, and legacy
  Tasks retain field omission. FINDING-037 is resolved; recovery remains a
  separate work order.
- WO-092 implements internal explicit recovery selected by
  OWNER-DECISION-015. Recovery validates the complete identified Objective,
  Plan, Queue, and Task relationship before mutation; retries the one failed
  item and its later pending remainder; synchronizes durable Plan and Queue
  state; and keeps Objective lifecycle ownership in ExecutionManager. Ordinary
  processing now skips pending work from failed identified attempts while
  continuing unrelated and legacy work. FINDING-036 is resolved for identified
  attempts; legacy unidentified records remain deliberately nonrecoverable.
- WO-093 assesses the application-facing recovery boundary. PROPOSAL-010
  recommends Option A: a canonical-ID-only OperationalSession method that
  delegates directly through a narrow Executive recovery service, returns the
  canonical Objective, and leaves Kernel and CLI unchanged. No product code or
  API changed; DECISION-REQUEST-017 requires owner selection.
- OWNER-DECISION-017 selects Option A. WO-094 records a canonical-ID-only
  OperationalSession recovery method that will delegate through a narrow
  ExecutiveManager recovery service directly to ExecutionManager, return the
  canonical completed Objective, and leave Kernel and CLI unchanged. No product
  code or API changed; implementation remains a separate work order.
- WO-095 implements OWNER-DECISION-017. OperationalSession now exposes explicit
  Objective-ID recovery and returns its canonical Objective. ExecutiveManager
  delegates to the same ExecutionManager used by the composed pipeline, without
  invoking the normal pipeline. Kernel and CLI remain unchanged.
- WO-096 rehearses a real execution failure followed by reload and recovery.
  FINDING-038 blocks this path: ordinary execution skips Plan persistence when
  Queue processing raises. Recovery rejects the resulting stale Plan state.
  Prior tests used coherent prepared state; they did not prove this lifecycle.
  The disposable workspace was removed and active data remained unchanged.
- WO-097 resolves FINDING-038: ordinary queue failure now persists Plan Task
  transitions while preserving the original exception. Real failure, reload,
  and application recovery now succeed; completed work remains untouched.
- WO-098 assesses a one-shot recovery CLI. PROPOSAL-011 recommends explicit
  workspace and Objective ID with exit statuses 0/1/2. DECISION-REQUEST-018
  requires owner selection; ID discovery is a separate acknowledged gap.
- WO-099 records OWNER-DECISION-018 selecting Option A: the explicit-workspace,
  exact-ID one-shot recovery CLI. Implementation remains a separate work order;
  no source or API changed in this checkpoint.
- WO-100 implements the approved one-shot recovery CLI with exact workspace/ID
  selection, 0/1/2 statuses, safe failure diagnostics, and a canonical Objective
  summary. Actual failed execution followed by CLI recovery passes.
- WO-101 assesses read-only Objective discovery. PROPOSAL-012 recommends complete
  workspace-scoped listing of ID, status and goal, with legacy identity preserved
  and no execution or recovery. DECISION-REQUEST-019 awaits owner selection.
- WO-102 records OWNER-DECISION-019 selecting Option A: read-only complete
  Objective listing in an explicit workspace. Implementation remains a separate
  work order; no product code changed in this decision checkpoint.
- WO-103 implements OWNER-DECISION-019. The read-only objectives CLI lists all
  persisted records with safely quoted identity, status and goal, including
  repeated goals and legacy null IDs, while verified to make no workspace writes.
- WO-104 assesses CLI Objective-ID reporting. PROPOSAL-013 recommends explicit
  OperationalSession create/execute steps with compatible execute_goal, allowing
  ID output before execution. DECISION-REQUEST-020 awaits owner selection.
- WO-105 records OWNER-DECISION-020 selecting Option A: explicit session creation
  and canonical execution, compatible execute_goal, and CLI ID reporting before
  execution. No product code changed in this decision checkpoint.
- WO-106 implements OWNER-DECISION-020: explicit session creation/execution,
  compatible execute_goal, flushed CLI ID before execution, and safe failure
  diagnostics. The reported failure ID is verified usable for recovery.
- WO-107 passes the disposable operator failure/discovery/recovery/rediscovery
  rehearsal, preserving completed work and active data. See VERIFICATION-100.
- WO-108 assesses operational readiness: the default SystemCapability performs
  lifecycle transitions, not actual app building. A bounded executable-task
  acceptance contract is the recommended next step, not yet approved.
- WO-109 proposes Task-owned typed executable intent (Option A) for one
  deterministic source-file build and direct-Python verification. Owner
  approval was required before implementation.
- OWNER-DECISION-021 approves WO-109 Option A and all ten acceptance rules.
  WO-110 records the decision; implementation remains a separate work order.
- WO-111 implements the approved opt-in, Task-owned print-only Python-file
  intent with confined atomic creation, direct verification, bounded evidence,
  truthful lifecycle failure and no-overwrite recovery behavior.
- Current verification passes 191 tests, compile and 188 QAOS imports; active
  data remains unchanged. See VERIFICATION-101.
- WO-112 finds that mixed ordinary/executable skills cannot safely use the
  current first-registered SkillResolver behavior. Option A proposes explicit
  intent-type routes with fail-closed resolution.
- WO-113 records OWNER-DECISION-022 approving Option A and its resolver-only
  implementation boundary. No product code changed in this checkpoint.
- WO-114 implements immutable explicit skill routes with fail-closed typed
  resolution and preserved legacy behavior. 206 tests, compile and 188 imports
  pass; active data is unchanged. See VERIFICATION-102.
- WO-115 proposes an explicit output-workspace opt-in on create_executive,
  enabling only instance-local Python-file capability and routing. Owner
  approval is recorded in OWNER-DECISION-023; executable Task submission remains
  a separate gap. WO-116 records this decision without product changes.
- WO-117 implements the explicit factory opt-in with per-instance routing and
  output binding, preserving defaults and global registries. 213 tests, compile
  and 188 imports pass; active data unchanged. See VERIFICATION-103.
- WO-118 proposes explicit session-owned Objective/intent submission through
  the existing Executive pipeline and PlannerManager-owned one-task planning.
  OWNER-DECISION-024 approves Option A and its explicit entry boundary. WO-119
  records the decision; no submission API has been implemented.
- WO-120 completes the public-session typed build through the existing pipeline.
  The owner-approved capability lifecycle extension resolves FINDING-039;
  target rejection and recovery refusal retain coherent failed states. 223 tests,
  compile and 188 imports pass; active data unchanged. See VERIFICATION-104.
- WO-121 verifies public-API build, discovery, collision and recovery refusal
  across five fresh processes. Successful work and active data are preserved;
  disposable directories removed. See VERIFICATION-105.
- WO-122 proposes one explicitly enabled, trusted text-statistics module
  template with fixed acceptance cases. Print-only behavior stays unchanged;
  OWNER-DECISION-025 approves Option A. WO-123 records the decision.
- WO-124 implements the explicitly enabled text_stats_v1 template through the
  existing public-session pipeline. All 245 tests, compile and 190 imports pass;
  active data is unchanged. Disabled reload recovery and corrupted source are
  rejected. See VERIFICATION-106; review was same-agent, not independent.
- The WO-108 regression run passes 182 tests. The architecture inspector no longer
  reports `ENTITY-OBJECTIVE-SELF-PERSISTENCE`; unrelated findings remain. See
  VERIFICATION-099.

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
2. WO-125 passes the six-process trusted-template rehearsal (VERIFICATION-107).
   WO-126 proposes a separately enabled text_stats_cli_v1 single-file app.
   OWNER-DECISION-026 approves Option A and its boundaries; WO-127 records it.
   WO-128 implements it: 253 tests, compile and 192 imports pass; active data
   unchanged (VERIFICATION-108). WO-129 passes the eight-process CLI rehearsal
   and 253 regressions (VERIFICATION-109). WO-130 proposes a trusted four-file
   project with staged verification and no-replace publication. OWNER-DECISION-027
   approves Option A; WO-131 records it. WO-132 passes the local Windows/NTFS
   publication gate (VERIFICATION-110). WO-133 implements the approved project:
   285 tests, compile and 194 imports pass; active data unchanged. See
   VERIFICATION-111. WO-134 passes the nine-process project rehearsal and 285
   regressions (VERIFICATION-112). WO-135 proposes explicitly configured metric
   selection in project v2, preserving v1. OWNER-DECISION-028 approves Option A;
   WO-136 records it. WO-137 implements all seven v2 configurations with preserved
   v1: 307 tests, compile and 195 imports pass; active data unchanged. See
   VERIFICATION-113. WO-138 passes the nine-process configurable-project rehearsal
   and 307 regressions, with active data unchanged (VERIFICATION-114).
   WO-139 proposes an explicit opt-in v2 build CLI consuming the existing typed
   API. OWNER-DECISION-029 approves Option A and its boundaries; WO-140 records
   approval. Next: separately scoped explicit builder CLI implementation.
3. Do not infer production-provider readiness or expand into publishing, UI,
   retries, or other excluded features from this test-only slice.
4. Address any newly prioritized architecture finding only through its own
   evidence-backed work order.
5. Do not infer CLI or raw-goal authorization from WO-044; those remain separate
   future decisions.
