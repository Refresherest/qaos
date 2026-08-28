# FINDING-027 — Agent-to-Skill Global Dependencies

## Status

`RESOLVED — WO-054`

## Evidence

Agent always used the module SkillResolver, while SkillResolver and SkillManager
always used one module skill registry. An explicitly selected Agent could not
retain isolated skill ownership without replacing module state.

## Resolution

WO-054 introduces instantiable SkillRegistry state and explicit selection through
Agent, SkillResolver, and SkillManager. Default constructors and the built-in
planning-skill registration remain compatible.

## Boundary

Skill capability resolution, capability registry lifecycle, skill-selection
policy, and execution semantics are unchanged.
