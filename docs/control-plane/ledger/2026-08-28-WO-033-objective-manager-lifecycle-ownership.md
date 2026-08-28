# WO-033 — Objective Manager Lifecycle Ownership

## Objective

Remove Objective entity self-persistence so lifecycle changes persist only
through the explicitly selected ObjectiveManager and Stores boundary.

## Architectural Context

Objective methods currently import the default `objective_manager` and call its
private `_save`, even when the Objective belongs to an isolated manager. This
creates hidden global persistence and forces Content OS to mutate Objective
internals directly to protect active data.

## Approved Contract

1. Objective methods mutate Objective state only.
2. ObjectiveManager exposes assign, assign-plan, start, complete, and fail
   operations that call the entity transition and persist through that manager.
3. Default Council delegation explicitly uses the default ObjectiveManager.
4. Content OS explicitly uses its injected private ObjectiveManager.
5. Existing status values, timestamps, schema, and entity method names remain.

## Scope

- `qaos.objectives.Objective` and ObjectiveManager lifecycle ownership
- Council delegator's proven Objective assignment caller
- Content OS first-slice Objective lifecycle caller
- Focused isolated lifecycle and regression tests
- Finding, verification, current-state, and handoff records

## Explicit Non-Goals

- Do not change objective schema, statuses, transition validation, or identity.
- Do not redesign Council, execution, planning, or Content OS flow.
- Do not change active data, providers, models, or credentials.

## Acceptance Criteria

1. Objective entity methods contain no manager import or persistence call.
2. An isolated ObjectiveManager persists start/complete/fail only to its Stores.
3. Entity-only mutation does not accidentally persist.
4. Council delegation and Content OS use explicit manager lifecycle methods.
5. Full tests/imports/compile/architecture inspection pass; active data is
   unchanged and `ENTITY-OBJECTIVE-SELF-PERSISTENCE` is absent.

## Stop Condition

Stop after lifecycle ownership is independently reviewed and published.
