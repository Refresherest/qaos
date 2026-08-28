# QAOS Current State

**Recorded:** 2026-08-28 UTC

**Branch baseline:** `fecf534` (`feat/operational-builder-chain`)

**Core baseline:** `615cbbb` (`main`)
**Status:** Core recovery checkpoint established with two open storage-test
findings; Builder Chain named-profile validation is blocked before delegation
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
- Current verification passes 17 of 19 tests. One failure is an invalid test
  assumption that active `data/queue.json` is absent. The other exposes shared
  module-level memory-registry state contaminating an explicitly injected
  temporary store. See FINDING-003 and VERIFICATION-012.

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

The owner has identified Content OS as the intended first downstream product
that QAOS should build. The tracked control plane does not yet establish its
domain boundary, contract, dependency order, or acceptance criteria. Content
OS implementation is therefore not authorized until the CSA issues a separate
bounded work package and the owner approves it.

## Open Priorities

1. Obtain OpenHands platform evidence for the parent-runtime startup failure;
   do not change QAOS profiles or product code in response to that failure.
2. Define and owner-approve a bounded Content OS architectural
   characterization work order before implementing downstream-product code.
3. Define a separate work order to repair and verify explicit manager/storage
   isolation before using that boundary for a downstream product.
4. Address pre-existing dead `qaos.queue.queue_db` and registry string-key
   findings only through separate work orders if they become prioritized.
