# WO-018 — OpenHands Named Role-Profile Smoke Test

## Identifier

`SMOKE-002`

## Objective

Determine whether a fresh OpenHands Cloud Builder Chain run can resolve the
owner-tested named profiles `QAOS_CSA`, `QAOS_PE`, and `QAOS_REVIEWER` through
sequential CSA -> PE -> Reviewer delegation.

## Architectural Context

SMOKE-001 proved sequential file-based-agent orchestration with
`model: inherit`, but did not prove delegated named-profile resolution. The
owner reports that OmniRoute and all three matching OpenHands profiles have
now passed end-to-end smoke tests. SMOKE-002 is a bounded transport and
orchestration check; it does not change QAOS model governance or product
architecture.

## Scope

- Bind CSA primary and fallback agents to `QAOS_CSA`.
- Bind PE primary and fallback agents to `QAOS_PE`.
- Bind Reviewer primary and fallback agents to `QAOS_REVIEWER`.
- Update the Builder Chain document to record the bounded operating mode.
- Publish the branch and run one fresh no-change OpenHands Cloud
  CSA -> PE -> Reviewer smoke test.
- Record the exact outcome and working-tree evidence.

## Explicit Non-Goals

- Do not inspect, create, alter, or expose credentials.
- Do not change OmniRoute or OpenHands provider/profile settings.
- Do not modify QAOS product code or tests.
- Do not infer model `VALIDATED` or `DESIGNATED` status.
- Do not claim provider-level fallback from same-profile fallback agents.
- Do not repair unrelated working-tree changes.

## Implementation Requirements

1. Use only the three exact owner-provided profile names.
2. Preserve the existing one-primary, one-fallback-per-stage policy.
3. Preserve all unrelated working-tree changes.
4. If delegated named-profile resolution fails, immediately restore all six
   agent files to `model: inherit`, publish the restoration, record the exact
   failure, and stop.

## Verification Requirements

1. Confirm the six frontmatter `model` values match the approved mapping.
2. Confirm the Builder Chain table matches the agent files.
3. Run Markdown/frontmatter inspection, a credential-pattern scan limited to
   the scoped changes, and `git diff --check`.
4. Push `feat/operational-builder-chain`.
5. In one fresh OpenHands Cloud conversation, request a no-change bounded
   work package, implementation package, and independent review package.
6. Record stage reachability, exact technical errors if any, Reviewer verdict,
   repository-change result, and whether restoration was required.

## Acceptance Criteria

1. The six agents and Builder Chain document agree on the three mappings.
2. The branch is published before the Cloud run.
3. One fresh run either reaches CSA, PE, and Reviewer with a final verdict, or
   produces a reproducible named-profile-resolution failure.
4. A named-profile-resolution failure leaves the published branch restored to
   `model: inherit`.
5. No credentials, provider settings, QAOS product code, or unrelated changes
   are modified.

## Stop Condition

Stop after recording the first fresh Cloud result and, if required, publishing
the `model: inherit` restoration. Do not retry the same run or begin product
work.
