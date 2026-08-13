# PROPOSAL-003: WO-009 explicit storage construction boundary

- Timestamp: 2026-08-13 UTC
- Work order: WO-009
- Status: proposed
- Authority: Owner review required
- Related verification: VERIFICATION-010

## Finding

WO-009 established that active JSON storage is currently constructed at import time through module-level JSONStore instances in qaos.storage.database, while seven domain managers consume those instances directly.

An additional direct construction path exists in qaos.planner.plan_db.

## Proposed architectural boundary

The preferred future construction boundary is:

create_stores(data_dir) -> explicit storage collection

## Intended architectural effect

The proposed boundary would make storage construction explicit and allow the runtime to provide the data directory and resulting storage collection to consumers instead of relying on module-level construction as the active ownership mechanism.

The proposal is intended to support controlled storage construction, isolated test storage, and clearer separation between storage configuration and domain-manager behavior.

## Constraints

- Preserve existing JSON storage semantics.
- Preserve existing persisted data.
- Do not modify existing data/*.json files as part of the boundary change.
- Do not perform schema migration under WO-009.
- Do not refactor unrelated managers, registries, or runtime components.
- Any implementation must be separately authorized by an implementation work order.

## Authorization status

This record is a proposal only.

WO-009 does not authorize implementation of the proposed store factory.

No application behavior is changed by this record.

## Required next step

Owner review is required before an implementation work order is issued.
