# WO-020 — Memory Manager Storage Isolation

## Objective

Repair the reproduced MemoryManager lifecycle defect so a manager constructed
with an explicit `Stores` collection does not read from or persist objects from
the active module-level memory registry.

## Architectural Context

WO-010 made storage construction explicit, but FINDING-003 proves that
`MemoryManager(stores=...)` still shares the module-level registry populated by
the default import-time manager. Storage-path injection therefore does not
currently provide isolated manager state.

The existing default `memory_manager` and public memory module API are active
callers and must remain compatible. This work order establishes a narrow
contract for Memory only before considering the same pattern in other domains.

## Approved Contract

1. The default module-level `memory_manager` continues to use the default
   module-level memory registry and active data directory.
2. `MemoryManager()` without injected dependencies preserves existing behavior.
3. `MemoryManager(stores=explicit_stores)` uses a new private memory registry by
   default and persists only objects owned by that manager lifecycle.
4. `MemoryManager(stores=..., registry=...)` may use an explicitly supplied
   registry for deterministic composition and testing.
5. Existing module-level registry functions remain compatibility wrappers over
   the default registry instance.

## Scope

- `src/qaos/memory/registry.py`
- `src/qaos/memory/manager.py`
- Focused storage-boundary tests
- WO-020 verification and handoff records
- Current-state records required to close FINDING-003 accurately

## Explicit Non-Goals

- Do not refactor the other six storage-backed managers or registries.
- Do not remove the default `memory_manager` singleton.
- Do not change JSON schemas or active persisted data.
- Do not redesign the broader QAOS registry architecture.
- Do not modify Content OS, OpenHands, models, providers, or credentials.
- Do not repair unrelated registry string-key behavior.

## Acceptance Criteria

1. The reproduced explicit-store test persists only the new isolated memory.
2. Pre-populated default registry objects do not leak into an explicit manager.
3. Two explicit managers backed by different stores do not contaminate each
   other.
4. The default module registry compatibility functions still operate against
   the default registry.
5. The active `data/*.json` files are unchanged by verification.
6. Focused and full regression tests pass using a controlled writable temp root.
7. Compile, package-import, JSON, architecture inspection, and whitespace checks
   pass or exact unrelated findings are recorded.

## Stop Condition

Stop after MemoryManager isolation is implemented, independently reviewed, and
published. Treat other manager/registry domains as separate future work.
