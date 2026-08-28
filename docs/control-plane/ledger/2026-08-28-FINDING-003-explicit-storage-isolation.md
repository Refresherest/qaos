# FINDING-003 — Explicit Storage Isolation Is Incomplete

## Classification

`implementation-violation`

## Severity

`P1` for downstream-product readiness; no evidence of new persisted-data
corruption was produced by this inspection.

## Evidence

The controlled regression command was:

```text
.venv\Scripts\python.exe -m pytest -q -p no:cacheprovider --basetemp <writable-path>
```

Result:

```text
2 failed, 17 passed
```

`test_manager_accepts_explicit_stores` constructs
`MemoryManager(stores=create_stores(tmp_path))`, creates `alpha`, and expects
the supplied temporary store to contain that memory first. It instead contains
the pre-existing active-data memory titled `Hello`.

`src/qaos/memory/manager.py` imports a module-level registry and creates
`memory_manager = MemoryManager()` at import time. That default manager loads
the active `data/memory.json` records into the shared registry. A later manager
with an explicitly injected `Stores` collection writes all entries from that
shared registry into its temporary store.

Therefore, injecting an isolated storage collection does not establish an
isolated manager lifecycle.

The second failure, `test_create_stores_does_not_touch_active_data_dir`, asserts
that `data/queue.json` does not exist. That file legitimately pre-exists in the
authoritative checkout. The test checks absence rather than checking that the
active file's content and metadata remain unchanged.

## Scope Decision

WO-019 is documentation-only. It does not authorize changes to managers,
registries, storage, tests, or import-time construction. Both failures are
recorded unchanged.

## Recommended Future Work

Issue a separate CSA work package that establishes the intended manager and
registry isolation contract, then repairs the tests and implementation within
that approved boundary. Do not opportunistically patch only the assertion or
clear global state in a test without deciding the production lifecycle
contract.
