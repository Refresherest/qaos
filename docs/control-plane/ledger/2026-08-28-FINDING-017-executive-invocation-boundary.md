# FINDING-017 — Executive Invocation Boundary

## Status

`OPEN — OWNER DECISION REQUIRED`

## Evidence

- Runtime can retain an explicitly composed executive service.
- Kernel can use an explicitly bounded Dispatcher.
- No established Kernel or CLI operation invokes `runtime.get("executive")`.
- The existing `run <member>` command invokes a Council member by name.
- ExecutiveManager expects a canonical Objective, not a member name or raw goal.

## Impact

Reusing `run` would silently change a public command contract. Adding a goal-based
CLI command would also require decisions about Objective creation, persistence,
failure output, and result presentation. The repository does not authorize those
choices yet.

## Required Resolution

The owner selects DECISION-REQUEST-003 Option A, B, or C. No product-code fix is
authorized until that selection is recorded.
