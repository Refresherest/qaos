# OWNER-DECISION-019 — Read-Only Objective Discovery

## Decision

The owner selected Option A from DECISION-REQUEST-019 and adopts the complete
recommended contract and implementation boundary in PROPOSAL-012.

## Governing Requirements

- `python -m qaos.main objectives --workspace <path>` requires exact arguments
  and a nonblank existing workspace; usage errors exit 2, path/read errors exit 1.
- Explicit Stores and isolated ObjectiveManager enumerate objective_records in
  persisted order, retaining repeated goals and all legacy records.
- Show ID, status and goal with unambiguous quoting and escaped control
  characters. Preserve exact IDs; missing IDs are null/unidentified.
- Never assign IDs, save, create directories/data files, execute, or recover.
  Do not construct OperationalSession, Executive graph or a new Kernel for listing.
- Successful listing exits 0, including an explicit empty result. Load all
  records before output; malformed input, duplicate IDs and invalid JSON fail
  without partial listing, repair, or normal traceback.
- Report status only, not recovery eligibility. Exclude credentials, provider
  configuration, environment dumps and other stores from intentional output.

## Scope

Authorize a separate work order for main.py, one listing adapter, CLI/subprocess
tests and records. Prove no file creation or content/modification-time changes in
selected and active workspaces. No recovery changes, ID generation, migration,
filters, application API expansion, UI, automatic retry or audit evidence.
