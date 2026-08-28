# FINDING-029 — Default System Capability Is Unregistered

## Status

`RESOLVED — WO-056`

## Evidence

The built-in planning Skill names capability `system`, and a SystemCapability
instance exists, but no tracked source registers that instance in the default
capability registry. Executing the built-in planning Skill therefore raises
`RuntimeError: Capability 'system' not registered.`

## Impact

Explicitly composed capabilities are unaffected. The default Agent-to-Skill-to-
Capability execution path cannot complete using its built-in objects.

## Resolution

WO-056 applies the repository's established built-in package-initialization
pattern: `qaos.capabilities` registers the existing `system_capability` in the
default registry. A clean-process regression test proves the complete default
Agent-to-Skill-to-Capability execution path.
