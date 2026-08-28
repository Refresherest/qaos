# QAOS Current State

**Recorded:** 2026-08-28 UTC

**WO-023 base:** `bc9ab99` (`feat/operational-builder-chain`)

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
- Current verification passes 25 tests, including 11 focused
  storage-boundary tests. See VERIFICATION-016.

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

The owner has accepted PROPOSAL-004 through OWNER-DECISION-001. Content OS is a
downstream consumer of QAOS, and `Brief -> Reviewed Draft Artifact` is the
approved first slice. External publishing is excluded; readiness Gates 2–5
must pass first; and `ACCEPT`, `REVISE`, and `BLOCKED` are the accepted review
terms for now. Content OS implementation remains gated, not yet authorized.

## Open Priorities

1. Obtain OpenHands platform evidence for the parent-runtime startup failure;
   do not change QAOS profiles or product code in response to that failure.
2. Continue readiness Gate 2 one dependency at a time. Memory, Artifact, and
   Objective isolation are proven; Plan workspace isolation remains pending.
3. After Gate 2, establish the injected deterministic generation contract and
   end-to-end success/failure evidence required by Gates 3–5.
4. Address pre-existing dead `qaos.queue.queue_db` and registry string-key
   findings only through separate work orders if they become prioritized.
