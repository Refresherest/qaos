# HANDOFF-008 — OpenHands Inherited-Model Smoke Test

## Current State

WO-017 changes all QAOS file-based sub-agents to `model: inherit`. In an
OpenHands Cloud conversation, this causes CSA, PE, Reviewer, and their bounded
fallback agents to use the parent conversation model rather than requiring the
delegated runtime to resolve a saved named profile.

## What This Can Prove

- Agent-file discovery and registration.
- Sequential CSA -> PE -> Reviewer delegation.
- Package handoffs, stop conditions, and no-change review discipline.

## What This Cannot Prove

- Independent models by role.
- Provider diversification.
- Ordered LLM fallback chains.
- QAOS model validation or designation.

## Required Next Action

Pull this commit in a fresh OpenHands conversation, select the previously
working parent model profile, and run SMOKE-001 once. Record the exact stage
reachability, reviewer verdict, and clean-working-tree result.

## Later Production Path

Establish a controlled OpenHands SDK or Agent Server deployment with an
explicit LLM Profile Store and model-level fallback strategy. Do not restore
named `model:` entries in the Cloud-only setup until that store is available to
delegated sub-agents.
