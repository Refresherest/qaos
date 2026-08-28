# WO-060 — Operational Composition Root Decision

## Objective

Identify the missing production composition boundary and obtain an owner choice
before introducing a new public factory.

## Architectural Context

The full explicit runtime is verified, but its dependency graph exists only in
an integration test. The repository does not authorize which layer should own a
reusable production composition root.

## Scope

- Inspect existing Runtime, Kernel, Executive, and integration contracts
- Record bounded composition-root options and recommendation
- Update current state and handoff records

## Explicit Non-Goals

- No production code, public API, test, schema, provider, model, credential, or
  Content OS change.

## Verification Requirements

- Confirm no tracked production composition API already exists.
- Confirm each option preserves provider neutrality and established authority.
- Validate control-plane JSON, whitespace, and secret boundaries.

## Stop Condition

Stop after DECISION-REQUEST-004 is published. Implementation requires the
owner's explicit option selection.
