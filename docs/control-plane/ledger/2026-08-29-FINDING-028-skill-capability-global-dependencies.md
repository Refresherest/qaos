# FINDING-028 — Skill-to-Capability Global Dependencies

## Status

`RESOLVED — WO-055`

## Evidence

Skill always resolved through the module CapabilityManager, and CapabilityManager
always used one module capability registry. An explicitly selected Skill could
not retain isolated capability ownership without replacing module state.

## Resolution

WO-055 introduces instantiable CapabilityRegistry state and explicit selection
through Skill and CapabilityManager. Default constructors retain the established
module services.

## Boundary

Default capability registration, capability execution semantics, operations,
and provider/model behavior are unchanged.
