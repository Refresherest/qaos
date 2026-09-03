# OWNER-DECISION-021 — Executable Task Contract

## Date

2026-09-03

## Authority

Qaasim April, repository owner

## Decision

The owner selected **WO-109 Option A** and approved its ten acceptance rules.

Executable intent will be an optional, provider-neutral, serializable part of
the existing Task. QueueItem remains a non-owning carrier/reference for the
Task. A specifically registered capability will validate and execute the first
bounded intent. Human-readable Task descriptions will not be parsed as commands.

The first implementation is limited to one deterministic `.py` source file in
an explicit disposable workspace and one direct invocation of the current
Python interpreter with exact-output acceptance. The path, atomic-write,
no-overwrite, validation, evidence, lifecycle, failure, compatibility and
active-data isolation requirements are exactly those in WO-109.

## Boundaries

This decision does not authorize arbitrary shell commands, autonomous coding,
production models/providers, credentials, network access, package installation,
Git operations, external publishing, UI, GPU use, schema migration, exactly-once
side effects, or Content OS expansion.

## Consequence

A separate Principal Engineer work order may implement and verify this contract.
It must reuse Task, QueueItem, Capability and current lifecycle ownership; stop
when the one deterministic fixture and compatibility/regression checks pass.
