# WO-089 — Task Identity Recovery Precondition

## Objective

Verify that persisted Plan and Queue state can satisfy OWNER-DECISION-015's
coherent failed-Task reset requirement before implementing recovery.

## Architectural Context

Recovery is durable across persisted state. Plan and Queue currently serialize
Task state independently, while Objective identity correlates only the attempt.

## In Scope

- inspect Task construction and serialization;
- inspect Plan Task and QueueItem action persistence;
- run one bounded reload/reset characterization probe;
- record any blocking source-of-truth gap;
- propose alternatives and request an owner decision.

## Non-Goals

- product code, tests, entities, APIs, registries, or schemas;
- recovery, ordinary-processing guards, migration, or legacy association;
- inferred correlation from text, position, or timestamps;
- providers, models, credentials, OpenHands profiles, or deployment.

## Verification Requirements

- use isolated workspace-local probe data;
- verify object identity and independent state after reload;
- remove probe data;
- confirm active data, JSON, whitespace, secrets, and scope remain unchanged.

## Stop Condition

Stop when the precondition is proven or disproven and any required architectural
decision is recorded. Do not implement partial or live-process-only recovery.
