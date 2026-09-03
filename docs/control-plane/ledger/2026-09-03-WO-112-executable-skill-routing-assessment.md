# WO-112 — Executable Skill Routing Assessment

Baseline: 33e8c4f on feat/operational-builder-chain, 2026-09-03.

Objective: identify the next smallest builder increment after WO-111. Scope is
read-only assessment, options and owner decision request. No product code,
tests, runtime registration, executable authority, provider, credential, CLI,
Git, Content OS or schema changes.

## Evidence

WO-111 proves the Python-file capability through a deliberately isolated graph
containing one skill. The production `create_executive` graph registers only
the ordinary planning/system skill. `SkillResolver.resolve()` returns the first
registered skill and does not inspect Task intent. `OperationalSession` offers
goal execution but has no approved way to submit a prepared executable Task.

Therefore, registering both ordinary and Python-file skills today would make
execution depend on insertion order: executable Tasks could be completed by
SystemCapability without building a file, or ordinary Tasks could be sent to a
capability that correctly rejects them. WO-111 must not be wired into the
operational session until routing is explicit.

## Options

### Option A — Explicit intent-type skill routes (recommended)

Extend the existing SkillResolver with an injected, immutable mapping from
validated intent type to registered skill name plus one explicit default skill
name for Tasks without intent. Resolution rules:

1. A Task without intent resolves only to the configured default skill.
2. A Task with intent resolves only through its exact intent type.
3. Missing default, missing route, unknown type or missing routed skill fails
   closed before capability execution.
4. Routing does not inspect Task.description, objective text, provider/model,
   registry insertion order or arbitrary attributes.
5. Existing construction without an injected route retains its current
   first-skill compatibility behavior; production composition remains unchanged
   in this work order.

Consequence: the existing Agent -> Skill -> Capability chain remains intact;
routing becomes deterministic and testable without granting any capability.
The mapping is local composition data, not a new registry or global source of
truth.

### Option B — Agent dispatches directly to Capability

Teach Agent to inspect intent and bypass Skill. This collapses established role
boundaries and duplicates capability resolution. Reject.

### Option C — Reserve registry order

Document that the first skill must match every workload. This cannot safely
support mixed ordinary/executable Tasks and preserves hidden ordering. Reject.

## Acceptance boundary if Option A is approved

A separate implementation work order changes only SkillResolver and focused
composition tests. It proves explicit default routing, exact typed routing,
fail-closed missing/unknown routes, insertion-order independence, legacy
compatibility, no capability execution on resolution failure, and unchanged
default executive/session behavior. It does not register PythonFileCapability
in production or add an application-facing executable method.

## Decision request

Owner: approve, revise or reject **Option A — explicit intent-type skill routes**.
Approval authorizes only the bounded resolver implementation above. A later,
separate architectural decision would still be required to expose executable
Tasks through OperationalSession.

No tests were run because this assessment changes control-plane records only.
All unrelated working-tree changes remain untouched.
