# PROPOSAL-011 — One-Shot Recovery CLI

## Evidence

src/qaos/main.py handles objective separately from the legacy command registry,
requires --workspace, and returns 0/1/2. commands/objective.py constructs an
OperationalSession; the Kernel need not receive a new method. Recovery returns
a canonical Objective, not ExecutionResult, so success checks must use its
status rather than the unrelated ExecutionResult.completed flag.

## Recommended Contract

- Syntax: `python -m qaos.main recover --workspace <path> <objective_id>`.
- Require exactly one nonblank workspace and one nonblank ID; reject missing
  or extra arguments as usage errors (exit 2), before session construction.
- Preserve ID bytes; do not normalize IDs, join goal words, search by goal,
  select the latest failed attempt, or guess a workspace.
- Require an existing workspace directory before constructing Stores. Missing
  or invalid workspace is an operation failure (exit 1); do not create it.
- Delegate once to OperationalSession.recover_objective. Keep preflight,
  lifecycle, ordering, and persistence ownership unchanged.
- Success: exit 0 only for returned Objective status completed; print Objective
  ID, goal, and status. Existing worker output may precede this summary; this
  is human-readable output, not a machine-readable protocol.
- Failure: exit 1 with a concise stderr diagnostic; no fabricated success,
  implicit retry, or traceback in the normal CLI response.
- No credentials, environment dumps, request headers, or provider settings in
  command output. Do not add logging of configuration objects.
- Existing objective and legacy commands retain their contracts. Kernel remains
  unchanged. The explicitly supplied command is the manual recovery invocation;
  no additional interactive prompt or automatic loop is introduced.

## Identity Discovery Limitation

The current objective command does not print canonical IDs, including on failure.
This first adapter requires an already-known ID. A read-only listing/inspection
command or failure-ID reporting is separate work; never compensate by guessing
identity. Existing preflight rejects unknown and unidentified legacy records.

## Separate Work

If approved, implement only main.py, a recovery command adapter, focused CLI and
subprocess tests, and control-plane records. Prove real failure then recovery in
a disposable workspace. UI, ID discovery, historical repair, retry policy, and
durable audit evidence remain excluded.
