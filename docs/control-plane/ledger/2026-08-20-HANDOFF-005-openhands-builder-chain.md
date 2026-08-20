# HANDOFF-005: OpenHands Builder Chain

- Status: ready for Cloud validation
- Work order: WO-014
- Date: 2026-08-20

## Completed

- Added six OpenHands file-based agents under `.agents/agents/`:
  - `qaos-csa` and `qaos-csa-fallback`
  - `qaos-principal-engineer` and `qaos-principal-engineer-fallback`
  - `qaos-reviewer` and `qaos-reviewer-fallback`
- Added standard `WORK_PACKAGE`, `IMPLEMENTATION_PACKAGE`, and `REVIEW_PACKAGE` handoff templates.
- Added `docs/control-plane/OPENHANDS_BUILDER_CHAIN.md`, which defines sequential delegation, one bounded technical fallback per role, and at most one remediation cycle per work order.
- Candidate profiles are explicit and do not constitute QAOS model designation.

## Verification

- Required frontmatter shape: passed for all six agent files.
- Required unique role names: passed.
- Credential-assignment scan: passed.
- `git diff --check`: passed.

## Cloud Validation Required

After this bounded change is pushed, OpenHands Cloud must pull the branch and run a no-op objective through the builder chain. The run must demonstrate:

1. the custom agent files are loaded;
2. `qaos-csa` produces a work package;
3. `qaos-principal-engineer` and `qaos-reviewer` receive their handoffs; and
4. the reviewer returns a verdict without product-code changes.

## Current Live-Cloud Facts

- OpenHands sub-agent delegation was observed enabled.
- The Cloud LLM profile list includes `openhands/glm-5.2`, `openai/deepseek-v4-pro`, and `openai/qwen3-coder-plus`.
- OpenHands Cloud exposes individual profiles, but no native ordered provider-fallback field was observed. The repository protocol therefore implements the bounded stage-level fallback.
- The OpenHands Critic was observed disabled; enable it later as an additional advisory guard. It does not replace `qaos-reviewer`.

## Stop Condition

Stop after Cloud validation. Do not begin QAOS product work without a concrete owner objective and CSA-issued work package.
