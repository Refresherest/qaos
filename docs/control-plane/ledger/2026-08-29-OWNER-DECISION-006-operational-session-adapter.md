# OWNER-DECISION-006 — Operational Session Adapter

## Status

`ACCEPTED`

## Decision

The owner selected **Option A — One-Shot CLI Objective Adapter** from
DECISION-REQUEST-006.

QAOS may add one thin CLI operation over OperationalSession. It must require an
explicit workspace path, accept one goal, print a concise result summary, and
return deterministic success, execution-failure, and usage process statuses.

This decision does not authorize an implicit active-data workspace,
interactive mode, Content OS integration, provider/model selection,
credentials, fallback, retry, deployment, or remote execution.
