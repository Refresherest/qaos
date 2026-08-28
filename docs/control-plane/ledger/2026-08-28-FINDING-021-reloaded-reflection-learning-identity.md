# FINDING-021 — Reloaded Reflection Learning Identity

## Status

`OPEN — NOT IN WO-047 SCOPE`

## Evidence

ReflectionManager reloads persisted reflection objective identity as a string.
LearningEngine supports either an Objective or string, but Learner's diagnostic
message directly accesses `reflection.objective.goal`. Passing a reloaded
reflection through Learner therefore raises AttributeError before learning.

## Impact

The canonical live executive pipeline passes an Objective and is unaffected.
Learning directly from a persisted/reloaded reflection is not currently safe.

## Required Resolution

Characterize the intended persisted-reflection learning contract in a separate
work order. Do not infer that string identity should be rehydrated or that Learner
should normalize it without an explicit scope decision.
