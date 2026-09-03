# OWNER-DECISION-018 — One-Shot Recovery CLI

## Decision

The owner selected Option A from DECISION-REQUEST-018, adopting the contract in
PROPOSAL-011.

## Governing Contract

- Syntax: `python -m qaos.main recover --workspace <path> <objective_id>`.
- Require exactly one nonblank workspace and ID. Missing or extra arguments
  return usage exit 2 before session construction.
- Preserve the exact ID; never infer identity from goals or select a latest
  failed attempt. Never guess a workspace.
- Require an existing workspace directory before constructing Stores. Invalid
  or missing directories return operation exit 1 without creating them.
- Delegate once to OperationalSession.recover_objective. Keep recovery preflight,
  lifecycle, ordering, and persistence ownership unchanged.
- Return exit 0 only when the returned canonical Objective has status completed.
  Print Objective ID, goal, and status; existing worker output may precede this
  human-readable summary. Do not treat Objective.completed as a success flag.
- Failure returns exit 1 with a concise stderr diagnostic, no normal traceback,
  fabricated success, or implicit retry.
- Do not expose credentials, environment dumps, request headers, provider
  settings, or configuration objects in command output.
- Existing objective and legacy command behavior and Kernel remain unchanged.
  Invocation is explicit manual recovery; no extra interactive prompt or loop.

## Scope and Limitations

Authorize a separate implementation work order for main.py, one recovery command
adapter, focused CLI/subprocess tests, and control-plane records. Verify actual
failure followed by recovery in a disposable workspace.

The caller must already know the Objective ID. ID discovery, failure-ID reporting,
UI, historical repair, migration, retry policy, providers, and durable audit
evidence remain excluded.
