# WO-024 — Planner Manager Isolation

## Objective

Establish and verify private PlannerManager registry state for explicitly
stored workspaces as the final bounded dependency of Content OS readiness Gate
2.

## Architectural Context

OWNER-DECISION-001 requires an isolated objective-to-artifact workspace before
Content OS implementation. PlannerManager accepts `stores=...` but currently
uses a module-level registry populated by the default import-time manager. This
is the same lifecycle pattern corrected for MemoryManager, ArtifactManager, and
ObjectiveManager by WO-020, WO-022, and WO-023.

## Approved Contract

1. The default module-level `planner_manager` retains the active data directory
   and default compatibility registry.
2. `PlannerManager()` without injected dependencies preserves existing
   behavior.
3. `PlannerManager(stores=explicit_stores)` receives a private plan registry by
   default.
4. An explicit registry may be injected for deterministic composition.
5. Module-level registry functions remain compatibility wrappers over the
   default registry.

## Scope

- `src/qaos/planner/registry.py`
- `src/qaos/planner/manager.py`
- Focused storage-boundary tests
- Current-state, verification, and handoff records

## Explicit Non-Goals

- Do not modify plan generation, task behavior, or other manager domains.
- Do not redesign broader planner architecture or registry key semantics.
- Do not remove the default `planner_manager` singleton.
- Do not implement Content OS briefs, artifacts, reviews, or workflows.
- Do not change schemas, active data, providers, models, or credentials.

## Acceptance Criteria

1. Two explicitly stored PlannerManagers cannot observe or persist each
   other's plans.
2. Pre-existing default registry plans do not leak into explicit stores.
3. Default registry compatibility functions continue to operate.
4. Active `data/*.json` content and modification times are unchanged.
5. Focused and full regression tests, compilation, package imports,
   architecture inspection, JSON, secret, and whitespace checks pass.

## Stop Condition

Stop after PlannerManager isolation is published and reviewed. Gate 2 may be
declared passed if all acceptance criteria succeed, but Gate 3 work requires a
separate work order.
