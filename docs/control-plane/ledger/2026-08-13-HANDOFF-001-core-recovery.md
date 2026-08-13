# HANDOFF-001: QAOS Core Recovery

- Timestamp: 2026-08-13 UTC
- Repository: `C:\Projects\qaos`
- Base commit: `f729c1b2ec24c28229d67d1135996ab365902534` on `main`
- Working tree: contains the completed recovery changes and pre-existing
  untracked draft architecture materials; nothing in this handoff is committed
  or pushed.

## Mandatory reading order

1. `docs/control-plane/README.md`
2. `docs/control-plane/CURRENT_STATE.md`
3. `docs/control-plane/AUTHORITY_AND_RECONCILIATION.md`
4. this handoff and the active work order below

## Authority rule

The untracked `docs/architecture/` ADRs/reports and `docs/vision/` are
drafts/evidence only. They may be useful, but do not govern code changes. New
architecture contracts require executable evidence and fresh owner approval.

## Completed recovery work

- Explicit `create_configuration()` and `create_runtime()` core boundary.
- Kernel/CLI routed through that boundary; command arguments are forwarded.
- Exactly-once reflection/learning ownership restored to the executive pipeline.
- Retired unused duplicate runtime, container, and dormant persistence packages.
- Active JSON storage now rejects corrupt non-empty data and uses atomic writes.
- Repository-native control plane, evidence ledger, architecture inspector, and
  regression suite established.

## Verified command

```powershell
cd C:\Projects\qaos
.\.venv\Scripts\python.exe -m pytest
```

Last result: **14 passed**. Also verified: compile, 44-package import sweep,
architecture inspection, and `git diff --check`.

## Install if `.venv` is absent

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[test]"
```

## Next authorized task

`WO-009` is characterization only: map active `qaos.storage` construction and
manager ownership, then propose—not implement—an explicit store-factory
boundary. Do not migrate JSON files, remove manager writes, or normalize every
registry.

## Handoff constraints

- Preserve existing untracked material; do not use `git reset --hard` or broad
  cleanup commands.
- Stage/commit only files owned by the selected work order. Do not accidentally
  include `.codex/` or draft architecture material unless the owner explicitly
  chooses to version it.
- Record every command/result in a new verification ledger entry.
