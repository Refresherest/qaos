# WO-054 — Agent-to-Skill Composition

## Objective

Allow an explicitly composed Agent to resolve and execute skills from a
caller-selected skill lifecycle without crossing into module state.

## Architectural Context

WO-053 made worker-to-agent selection explicit. Agent, SkillResolver, and
SkillManager still selected the module resolver and registry internally.

## Requirements

1. SkillRegistry is instantiable; compatibility functions retain the default.
2. SkillManager and SkillResolver accept explicit SkillRegistry services.
3. Agent accepts an explicit SkillResolver-compatible service.
4. The selected skill executes and its return value passes through unchanged.
5. Default constructors preserve existing services and registration behavior.

## Scope

- Skill registry lifecycle
- Agent, SkillResolver, and SkillManager dependency injection
- Explicit execution, default compatibility, and registry-isolation tests
- Finding, verification, current-state, and handoff records

## Explicit Non-Goals

- No capability resolution, skill-selection policy, or execution-semantic change.
- No provider, model, credential, Content OS, or executive-stage change.

## Verification Requirements

- Prove a selected skill executes through a selected Agent and resolver.
- Prove explicit skill registries are isolated.
- Prove default compatibility.
- Run focused and full regression checks, import sweep, compilation,
  architecture inspection, and active-data comparison.

## Stop Condition

Stop after FINDING-027 is independently reviewed and WO-054 is published.
