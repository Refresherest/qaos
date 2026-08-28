# FINDING-020 — Learning Stage Global Dependencies

## Status

`RESOLVED — WO-047`

## Evidence

LearningManager called the module Learner, which called the module LearningEngine,
which wrote through default MemoryManager and KnowledgeManager objects. An
explicit executive pipeline could not retain isolated learning persistence.

## Resolution

WO-047 adds explicit dependency selection at all three learning layers and
proves writes against a caller-selected Stores collection while retaining defaults.

## Boundary

Learning content rules, title keying and overwrite semantics, deduplication, and
other executive stages remain outside this work order.
