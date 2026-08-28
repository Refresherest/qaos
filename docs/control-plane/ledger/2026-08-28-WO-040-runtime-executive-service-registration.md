# WO-040 — Runtime Executive Service Registration

## Objective

Make an explicitly composed executive service reachable through Runtime and
Kernel without changing dispatcher or CLI command semantics.

## Architectural Context

WO-039 established an injectable public ExecutiveManager. Runtime already owns
explicit service registration for logger and events, but has no executive input,
so Kernel cannot retain an explicitly composed executive in its service boundary.

## Approved Contract

1. create_runtime accepts an optional explicit executive service.
2. A supplied executive is registered under the stable `executive` service key.
3. Kernel forwards its optional executive input into runtime construction.
4. Omitted services remain absent; no default singleton is imported implicitly.
5. Existing logger, events, dispatcher, and execute behavior remain unchanged.

## Scope

- Runtime factory and Kernel optional executive composition
- Explicit registration and omission tests
- Finding, verification, current-state, and handoff records

## Explicit Non-Goals

- Do not route dispatcher or CLI commands through the executive service.
- Do not change command registry, handlers, Kernel.execute, or service keys.
- Do not implement a second Content OS slice or change providers or credentials.

## Acceptance Criteria

1. Runtime returns the exact explicitly supplied executive service.
2. Kernel retains the exact executive through its runtime.
3. Omitted logger, events, and executive services remain absent.
4. Existing command dispatch and full verification remain green.

## Stop Condition

Stop after runtime executive registration is independently reviewed and published.
