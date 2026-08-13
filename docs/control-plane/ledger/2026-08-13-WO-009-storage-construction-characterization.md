# WO-009: Characterize active storage construction and ownership

- Status: authorized
- Priority: P1
- Authority: owner recovery direction; Handoff-001
- Scope: tests and evidence records for `qaos.storage` construction and the
  seven active domain-manager store consumers.
- Non-goals: JSON migration, data deletion, changing the storage file schema,
  or a manager/registry-wide refactor.

## Acceptance criteria

1. Tests show how a manager/store binds to an explicit temporary data path.
2. The existing `data/*.json` files are not modified during testing.
3. A proposed `create_stores(data_dir)` contract is recorded for owner approval;
   no behavior-changing implementation occurs without that approval.
4. Full pytest, import sweep, inspector, compile, and whitespace checks are
   recorded.
