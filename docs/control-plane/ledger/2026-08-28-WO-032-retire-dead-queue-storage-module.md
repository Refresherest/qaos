# WO-032 — Retire Dead Queue Storage Module

## Objective

Remove the tracked, dead, and unimportable `qaos.queue.queue_db` module so the
package tree has one queue-storage construction boundary: `Stores.queue_db`.

## Architectural Context

QueueManager uses the explicit `create_stores(DATA)` boundary introduced by
WO-010. The separate `queue/queue_db.py` module is imported by no caller,
constructs storage at import time, and imports a nonexistent `JsonDatabase`.
Direct import raises `ModuleNotFoundError`.

## Scope

- Remove `src/qaos/queue/queue_db.py`.
- Add a regression guard proving the dead module is not importable.
- Verify the complete tracked QAOS package tree imports.
- Record the finding and update current-state evidence.

## Explicit Non-Goals

- Do not change QueueManager, queue registry, queue schema, or queue behavior.
- Do not modify active queue data.
- Do not change Content OS, providers, models, credentials, or other modules.

## Acceptance Criteria

1. `qaos.queue.queue_db` is absent and cannot be imported.
2. QueueManager continues to use `Stores.queue_db`.
3. The complete QAOS package import sweep passes without exclusions.
4. Focused/full tests and standard verification pass; active data is unchanged.

## Stop Condition

Stop after the dead module is retired, reviewed, and published.
