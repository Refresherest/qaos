# WO-010: Implement explicit storage construction boundary

- Timestamp: 2026-08-13 UTC
- Work order: WO-010
- Status: authorized
- Authority: Owner approval of PROPOSAL-003
- Related verification: VERIFICATION-010
- Related proposal: PROPOSAL-003

## Objective

Implement the approved explicit storage construction boundary identified by WO-009 and PROPOSAL-003.

## Authorized scope

- Introduce an explicit create_stores(data_dir) storage construction boundary.
- Move active JSONStore construction behind that boundary.
- Update the seven affected domain-manager consumers to use the explicit storage collection.
- Address the additional direct storage construction path in qaos.planner.plan_db.
- Preserve existing JSON storage semantics and persisted data.
- Add or update tests required to verify the new construction boundary.
- Verify isolated temporary-directory storage behavior.
- Verify existing data/*.json files are not modified by the implementation.

## Constraints

- No schema migration.
- No modification of existing persisted data as part of the implementation.
- No unrelated refactoring.
- No changes to unrelated runtime components.
- Preserve existing externally observable behavior unless required by the approved boundary.
- Do not broaden the work order without owner authorization.

## Acceptance criteria

- Storage construction is explicit rather than relying on module-level construction as the active ownership mechanism.
- All identified consumers use the approved construction boundary.
- The qaos.planner.plan_db construction path is resolved within scope.
- Existing storage tests continue to pass.
- New or updated tests demonstrate isolated storage construction.
- Existing persisted JSON files remain unchanged.
- Full applicable verification passes.
- No unrelated application behavior is changed.

## Required verification

- pytest -q
- python -m compileall -q src tests tools
- python tools/architecture_inspect.py
- git diff --check
- Verify data/*.json remains unchanged.

## Implementation authorization

Owner approval of PROPOSAL-003 authorizes implementation under this work order.

Implementation must remain within the scope and constraints defined above.

## Completion requirement

Upon implementation completion, create a verification record documenting the exact changes, tests, architectural boundary achieved, and confirmation that no unauthorized behavior or data changes occurred.
