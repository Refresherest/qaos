# FINDING-029 — Default System Capability Is Unregistered

## Status

`OPEN — NOT IN WO-055 SCOPE`

## Evidence

The built-in planning Skill names capability `system`, and a SystemCapability
instance exists, but no tracked source registers that instance in the default
capability registry. Executing the built-in planning Skill therefore raises
`RuntimeError: Capability 'system' not registered.`

## Impact

Explicitly composed capabilities are unaffected. The default Agent-to-Skill-to-
Capability execution path cannot complete using its built-in objects.

## Required Resolution

Establish the intended default capability-registration lifecycle in a separate
work order. Do not infer import-time registration, bootstrap registration, or a
different default capability without an explicit scope decision.
