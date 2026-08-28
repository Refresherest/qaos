# WO-047 — Learning Stage Composition

## Objective

Allow the LearningManager, Learner, and LearningEngine chain to use explicitly
selected MemoryManager and KnowledgeManager services while preserving behavior.

## Architectural Context

ExecutivePipeline accepts an explicit learning stage, but the tracked learning
chain crosses through three module-level objects and ultimately writes through
default memory and knowledge managers.

## Requirements

1. LearningEngine accepts explicit memory and knowledge managers.
2. Learner accepts an explicit LearningEngine.
3. LearningManager accepts an explicit Learner.
4. Omitted dependencies retain existing default objects.
5. Summary, success, failure, count, and current title-overwrite semantics remain.

## Scope

- Learning engine, learner, and manager dependency selection
- Explicit isolated-store and default-compatibility tests
- Finding, verification, current-state, and handoff records

## Explicit Non-Goals

- No learning content, keying, deduplication, or overwrite redesign.
- No MemoryManager or KnowledgeManager behavior change.
- No other pipeline stage, CLI, Content OS, provider, model, or credential change.

## Acceptance Criteria

1. An explicit chain writes only through its selected Stores collection.
2. Existing memory/knowledge counts and persisted overwrite behavior remain.
3. Default constructors retain existing services.
4. Full verification passes and active data remains unchanged.

## Stop Condition

Stop after learning-stage composition is independently reviewed.
