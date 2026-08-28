# OWNER-DECISION-003 — Executive Invocation Option A

## Date

2026-08-28

## Authority

Qaasim April, repository owner

## Decision

The owner selects DECISION-REQUEST-003 **Option A**.

1. Add a distinct programmatic `Kernel.execute_objective(objective)` operation.
2. The input is an existing canonical QAOS Objective.
3. Kernel resolves the explicitly registered Runtime `executive` service.
4. The operation returns that service's ExecutionResult unchanged.
5. Objective creation and persistence remain with the caller's selected
   ObjectiveManager.
6. The legacy dispatcher, CLI, and `run <member>` command remain unchanged.

## Consequence

FINDING-017 is authorized for implementation through one separate bounded work
order. This decision does not authorize a new CLI command, raw-goal conversion,
implicit Objective creation, or repurposing `run`.
