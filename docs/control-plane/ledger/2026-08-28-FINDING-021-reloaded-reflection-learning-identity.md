# FINDING-021 — Reloaded Reflection Learning Identity

## Status

`RESOLVED — WO-048`

## Evidence

ReflectionManager reloads persisted reflection objective identity as a string.
LearningEngine supports either an Objective or string, but Learner's diagnostic
message directly accesses `reflection.objective.goal`. Passing a reloaded
reflection through Learner therefore raises AttributeError before learning.

## Impact

The canonical live executive pipeline passes an Objective and is unaffected.
Learning directly from a persisted/reloaded reflection is not currently safe.

## Required Resolution

LearningEngine already established support for canonical Objective and string
identity. WO-048 applies the same normalization to Learner's diagnostic output
and proves persisted reload-to-learning behavior without rehydration or schema
change.
