# DECISION-REQUEST-006 — Operational Session Adapter

## Status

`OWNER DECISION REQUIRED`

## Evidence

OperationalSession is now the verified programmatic path from a goal to a
canonical Objective and ExecutionResult. No user-facing adapter consumes it.

The existing `python -m qaos.main` interface dispatches legacy commands and
does not define workspace selection, objective output, or process exit status.
The repository's active `data/` directory must not become an implicit target
for a new execution command.

## Decision

Choose the first adapter over OperationalSession.

### Option A — One-Shot CLI Objective Adapter (Recommended)

Add one CLI operation that requires an explicit workspace path and one goal,
constructs OperationalSession, executes once, prints a concise result, and
returns a deterministic process status.

Consequences:

- provides the first visible manual QAOS execution path;
- remains a thin presentation adapter over the verified application boundary;
- protects active data by requiring explicit workspace selection;
- requires bounded decisions about syntax, output fields, and exit codes in
  the implementation work order.

### Option B — Interactive Local Shell

Add a long-running prompt that holds one OperationalSession and accepts
multiple goals.

Consequences:

- supports repeated local use without reconstructing the graph;
- introduces session controls, interruption, history, recovery, and output
  policy before one-shot behavior is proven;
- creates a larger interface and test surface.

### Option C — Defer All Adapters

Keep OperationalSession programmatic only.

Consequences:

- adds no interface contract;
- applications can already integrate through Python;
- QAOS still has no direct manual path for exercising the operational chain.

## Recommendation

Select **Option A**. A one-shot CLI operation is the smallest useful adapter
and can establish output and failure semantics before any interactive shell.
It must require an explicit workspace rather than defaulting to active data.

## Explicitly Deferred

- exact command name and argument syntax;
- machine-readable versus human-readable output details;
- interactive mode and execution history;
- Content OS integration;
- provider/model selection, fallback, retry, deployment, and remote execution.
