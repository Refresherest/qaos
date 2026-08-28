# DECISION-REQUEST-003 — Executive Invocation Boundary

## Decision Required

Choose how callers should first invoke the explicit Runtime executive service.

## Option A — Programmatic Kernel Objective Invocation

Add a distinct `Kernel.execute_objective(objective)` operation. It accepts an
existing canonical QAOS Objective, resolves the explicitly registered executive
service, and returns its ExecutionResult. Objective creation and persistence stay
with the caller's selected ObjectiveManager. The legacy command dispatcher and
`run <member>` behavior remain unchanged.

**Consequence:** establishes the smallest provider-neutral runtime invocation
contract and preserves source-of-truth ownership. It does not yet expose the
operation through the CLI.

## Option B — New Goal-Based CLI Command

Add a new command such as `objective <goal>`. It would require an explicit
ObjectiveManager service, create and persist an Objective, invoke the runtime
executive, and define user-facing result and failure output.

**Consequence:** provides immediate CLI access, but introduces several contracts
at once: command naming, raw-goal validation, workspace selection, persistence,
and output/error presentation.

## Option C — Repurpose `run`

Change `run <member>` into objective execution or overload it to support both
member names and objective input.

**Consequence:** breaks or ambiguously expands the established Council-member
command and couples legacy command behavior to the new executive boundary.

## CSA Recommendation

Approve **Option A**. It completes the explicit Kernel-to-Runtime service path
with one canonical input and return type, preserves the existing CLI, and leaves
a future CLI adapter to a separate evidence-backed work order.

## Owner Response Requested

Approve Option A, B, or C. No implementation will begin until the selection is
recorded.

## Owner Disposition

The owner selected **Option A** on 2026-08-28. See OWNER-DECISION-003. This
authorizes a separate bounded implementation work order; it does not place the
implementation inside this historical decision request.
