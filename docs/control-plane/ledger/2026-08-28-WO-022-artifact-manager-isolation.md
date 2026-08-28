# WO-022 — Artifact Manager Isolation

## Objective

Establish and verify private ArtifactManager registry state for explicitly
stored workspaces as the first bounded dependency of Content OS readiness
Gate 2.

## Architectural Context

OWNER-DECISION-001 requires an isolated objective-to-artifact workspace before
Content OS implementation. ArtifactManager accepts `stores=...` but currently
uses a module-level registry populated by the default import-time manager, the
same lifecycle pattern corrected for MemoryManager by WO-020.

The first approved Content OS slice must produce exactly one draft artifact
without observing or persisting artifacts from another workspace.

## Approved Contract

1. The default module-level `artifact_manager` retains the active data directory
   and default compatibility registry.
2. `ArtifactManager()` without injected dependencies preserves existing
   behavior.
3. `ArtifactManager(stores=explicit_stores)` receives a private artifact
   registry by default.
4. An explicit registry may be injected for deterministic composition.
5. Module-level registry functions remain compatibility wrappers over the
   default registry.

## Scope

- `src/qaos/artifacts/registry.py`
- `src/qaos/artifacts/manager.py`
- Focused storage-boundary tests
- Current-state, verification, and handoff records

## Explicit Non-Goals

- Do not modify ObjectiveManager, PlannerManager, or other manager domains.
- Do not fix the known string-key registry behavior.
- Do not remove the default `artifact_manager` singleton.
- Do not implement Content OS artifacts, briefs, reviews, or workflows.
- Do not change schemas, active data, providers, models, or credentials.

## Acceptance Criteria

1. Two explicitly stored ArtifactManagers cannot observe or persist each
   other's artifacts.
2. Pre-existing default registry artifacts do not leak into explicit stores.
3. Default registry compatibility functions still operate through the existing
   entity-object key path.
4. Active `data/*.json` content and modification times are unchanged.
5. Focused and full regression tests, compilation, package imports,
   architecture inspection, JSON, secret, and whitespace checks pass.

## Stop Condition

Stop after ArtifactManager isolation is published and reviewed. Gate 2 remains
incomplete until separately scoped objective and planning dependencies pass.
