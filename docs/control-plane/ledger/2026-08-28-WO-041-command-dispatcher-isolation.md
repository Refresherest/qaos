# WO-041 — Command Dispatcher Isolation

## Objective

Allow Kernel command dispatch to use an explicitly selected command mapping and
dispatcher while preserving all default CLI command semantics.

## Architectural Context

Dispatcher is instantiable but always reads the module-level COMMANDS mapping,
and Kernel always constructs a default Dispatcher. Isolated runtimes cannot
select a bounded command surface without monkeypatching global state.

## Approved Contract

1. Dispatcher accepts an optional explicit command mapping.
2. An explicit empty mapping remains empty and does not fall back to defaults.
3. Kernel accepts an optional explicit dispatcher.
4. Omitted inputs retain the existing COMMANDS mapping and Dispatcher.
5. Handler arguments, unknown-command output, and boolean results remain.

## Scope

- Dispatcher command-map ownership and Kernel dispatcher selection
- Explicit mapping, empty mapping, and default compatibility tests
- Finding, verification, current-state, and handoff records

## Explicit Non-Goals

- Do not change command names, handlers, registry contents, or CLI help.
- Do not route commands through Runtime or the executive service.
- Do not implement a second Content OS slice or change providers or credentials.

## Acceptance Criteria

1. Kernel forwards arguments through an explicit dispatcher and mapping.
2. An explicit empty mapping returns false with existing unknown output.
3. Default Dispatcher retains the exact module COMMANDS mapping.
4. Full verification passes and active data remains unchanged.

## Stop Condition

Stop after command dispatcher isolation is independently reviewed and published.
