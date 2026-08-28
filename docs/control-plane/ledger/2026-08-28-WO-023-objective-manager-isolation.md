# WO-023 — Objective Manager Isolation

## Objective

Establish and verify private ObjectiveManager registry state for explicitly
stored workspaces as the next bounded dependency of Content OS readiness Gate
2.

## Architectural Context

OWNER-DECISION-001 requires an isolated objective-to-artifact workspace before
Content OS implementation. ObjectiveManager accepts `stores=...` but currently
uses a module-level registry populated by the default import-time manager. This
is the same lifecycle pattern corrected for MemoryManager by WO-020 and
ArtifactManager by WO-022.

## Approved Contract

1. The default module-level `objective_manager` retains the active data
   directory and default compatibility registry.
2. `ObjectiveManager()` without injected dependencies preserves existing
   behavior.
3. `ObjectiveManager(stores=explicit_stores)` receives a private objective
   registry by default.
4. An explicit registry may be injected for deterministic composition.
5. Module-level registry functions remain compatibility wrappers over the
   default registry.

## Scope

- `src/qaos/objectives/registry.py`
- `src/qaos/objectives/manager.py`
- Focused storage-boundary tests
- Current-state, verification, and handoff records

## Explicit Non-Goals

- Do not modify PlannerManager or other manager domains.
- Do not redesign Objective entity self-persistence.
- Do not fix the known string-key registry behavior.
- Do not remove the default `objective_manager` singleton.
- Do not implement Content OS briefs, artifacts, reviews, or workflows.
- Do not change schemas, active data, providers, models, or credentials.

## Acceptance Criteria

1. Two explicitly stored ObjectiveManagers cannot observe or persist each
   other's objectives.
2. Pre-existing default registry objectives do not leak into explicit stores.
3. Default registry compatibility functions still operate through the existing
   entity-object key path.
4. Active `data/*.json` content and modification times are unchanged.
5. Focused and full regression tests, compilation, package imports,
   architecture inspection, JSON, secret, and whitespace checks pass.

## Stop Condition

Stop after ObjectiveManager isolation is published and reviewed. Gate 2 remains
incomplete until the separately scoped planning dependency passes.
