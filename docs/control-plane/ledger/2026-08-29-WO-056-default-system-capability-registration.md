# WO-056 — Default System Capability Registration

## Objective

Register the existing built-in SystemCapability in the default capability
lifecycle so the established default execution chain can complete.

## Architectural Context

The Agents and Skills packages register their built-in default instances during
package initialization. Capabilities constructed `system_capability` but omitted
the equivalent registration, leaving the built-in planning Skill unresolved.

## Requirements

1. The capabilities package registers the existing `system_capability` once in
   the default CapabilityRegistry lifecycle.
2. The default CapabilityManager resolves `system` to that canonical instance.
3. A clean process completes default Agent-to-Skill-to-SystemCapability execution.
4. Explicit CapabilityRegistry isolation remains unchanged.

## Scope

- Default SystemCapability registration in `qaos.capabilities`
- Clean-process default-chain regression test
- Finding, verification, current-state, and handoff records

## Explicit Non-Goals

- No new bootstrap system or capability implementation.
- No capability operation, selection policy, provider, model, credential,
  Content OS, or executive-stage change.

## Verification Requirements

- Prove canonical default registration and complete default execution in a clean process.
- Run focused and full regression checks, import sweep, compilation,
  architecture inspection, and active-data comparison.

## Stop Condition

Stop after FINDING-029 is independently reviewed and WO-056 is published.
