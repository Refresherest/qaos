# QAOS Control Plane

This directory is the repository-native operating record for QAOS. It is the
entry point for any human or AI engineer before changing architecture or
implementation.

## Start here

1. Read `CURRENT_STATE.md` and `AUTHORITY_AND_RECONCILIATION.md`.
2. Run `python tools/architecture_inspect.py` from the repository root.
3. Read the current baseline in `ledger/` and open work orders.
4. Follow `AI_EXECUTION_AND_HANDOFF.md`; do not treat an old report as proof
   of the current checkout.

## Record types

| Record | Purpose |
| --- | --- |
| `ledger/` | Immutable-ish records of decisions, findings, verification, and handoffs. |
| `templates/` | Copyable records for new work; do not edit templates to record a case. |
| `CURRENT_STATE.md` | A concise, dated view of what is known now. |
| `PROJECT_STATE.json` | Machine-readable current state for tools and automations. |

The repository and reproducible command output are evidence. This control
plane coordinates work; it does not silently replace accepted ADRs or code.
