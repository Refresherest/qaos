# WO-055 — Skill-to-Capability Composition

## Objective

Allow an explicitly composed Skill to resolve and execute capabilities from a
caller-selected capability lifecycle without crossing into module state.

## Architectural Context

WO-054 made Agent-to-Skill selection explicit. Skill and CapabilityManager still
selected the module manager and registry internally.

## Requirements

1. CapabilityRegistry is instantiable; compatibility functions retain the default.
2. CapabilityManager accepts an explicit CapabilityRegistry.
3. Skill accepts an explicit CapabilityManager-compatible service.
4. Selected capability execution and return values remain unchanged.
5. Default constructors preserve existing services.

## Scope

- Capability registry lifecycle
- Skill and CapabilityManager dependency injection
- Explicit execution, default compatibility, and registry-isolation tests
- Finding, verification, current-state, and handoff records

## Explicit Non-Goals

- No default capability registration or bootstrap decision.
- No capability operations, execution semantics, provider, model, credential,
  Content OS, or executive-stage change.

## Verification Requirements

- Prove a selected capability executes through a selected Skill.
- Prove explicit capability registries are isolated.
- Prove default service compatibility.
- Run focused and full regression checks, import sweep, compilation,
  architecture inspection, and active-data comparison.

## Stop Condition

Stop after FINDING-028 is independently reviewed, FINDING-029 is recorded
unchanged, and WO-055 is published.
