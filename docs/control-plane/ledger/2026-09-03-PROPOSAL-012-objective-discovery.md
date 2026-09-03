# PROPOSAL-012 — Read-Only Objective Listing

## Evidence

ObjectiveManager.objective_records returns the complete registry record tuple;
objectives() instead returns latest-by-goal entries and can hide repeated goals.
Manager loading does not assign IDs to legacy records or save data. Stores and
JSONStore construction do not create data directories; JSONStore.load treats
missing/empty files as empty and rejects invalid JSON.

## Recommended Contract

- Syntax: `python -m qaos.main objectives --workspace <path>`.
- Exact argument count and nonblank workspace; usage failure exits 2 before
  manager construction. Require an existing directory; invalid path exits 1
  without creating it. No implicit active-data workspace.
- Construct explicit Stores and ObjectiveManager only, using its isolated
  registry and objective_records(), never latest-by-goal lookup.
- Do not construct OperationalSession, Executive graph, or a new Kernel instance
  to perform listing. Do not invoke execution, recovery, generation, or save.
- Enumerate every Objective in persisted order; show ID, status, and goal.
  Repeated goals retain separate rows; no filtering, sorting, or pagination yet.
- Show missing legacy IDs explicitly as null/unidentified; never synthesize IDs,
  write fields back, or advertise such records as recoverable.
- Escape control characters in displayed values so goals cannot inject terminal
  control sequences or impersonate additional rows. Use unambiguous quoted
  values, retaining exact IDs rather than truncating or normalizing them.
- Exit 0 on successful listing, including an empty workspace. Print an explicit
  empty result when the existing compatible loader returns no records.
- Load the complete collection before printing rows. Invalid JSON, duplicate IDs,
  malformed records, or read failure exit 1 with a concise safe stderr diagnostic
  and no partial listing or normal traceback. Do not repair input.
- This is a human-readable inventory, not a stable JSON API or recovery dry-run.
  Failed status alone is not proof of Plan/Queue coherence or recovery eligibility.
- No credentials, provider configuration, environment dumps, or other stores
  are intentionally included in output. Goal text is workspace-owned user data.

## Implementation Boundary

If approved, change main.py, one listing adapter, CLI/subprocess tests and ledger
records. Prove no file creation, content change, or modification-time change in
selected and active workspaces; test repeat goals, legacy IDs, empty and corrupt
input, terminal escaping, and complete enumeration.

Recovery, ID generation, migration, filters, public application API expansion,
UI, automatic retry and audit evidence remain excluded.
