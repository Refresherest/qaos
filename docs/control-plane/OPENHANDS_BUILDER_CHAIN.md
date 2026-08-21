# QAOS OpenHands Builder Chain

## Operational Roles

The project defines six OpenHands file-based sub-agents in `.agents/agents/`:

| Stage | Primary agent | Current smoke-test model | Technical fallback agent | Current smoke-test model |
| --- | --- | --- | --- | --- |
| Architecture | `qaos-csa` | `inherit` (parent conversation model) | `qaos-csa-fallback` | `inherit` (parent conversation model) |
| Implementation | `qaos-principal-engineer` | `inherit` (parent conversation model) | `qaos-principal-engineer-fallback` | `inherit` (parent conversation model) |
| Independent review | `qaos-reviewer` | `inherit` (parent conversation model) | `qaos-reviewer-fallback` | `inherit` (parent conversation model) |

For the current OpenHands Cloud smoke test, every sub-agent inherits the
parent conversation model. This deliberately avoids named-profile resolution
because Cloud delegation reported an empty profile store. It proves the
CSA-to-PE-to-Reviewer orchestration path only; it does not prove independent
role models or model-level fallback routing. The fallback *agents* are used
only for a technical agent/model execution failure (for example provider
error, authentication error, timeout, or malformed tool response), not for a
hard problem, disagreement, failed test, or an architectural block.

## Required Flow

```text
Objective
  -> qaos-csa
  -> WORK_PACKAGE
  -> qaos-principal-engineer
  -> IMPLEMENTATION_PACKAGE
  -> qaos-reviewer
  -> REVIEW_PACKAGE
  -> ACCEPT: stop / await next owner objective
  -> REJECT or BLOCKED: qaos-csa issues at most one remediation package
```

The parent OpenHands conversation is the orchestrator. It must delegate stages
sequentially, preserve the returned artifacts, and never substitute its own
judgment for the CSA or Reviewer.

## Retry and Fallback Policy

1. Invoke the stage's primary agent once.
2. If the task returns a technical execution error, invoke that stage's named
   fallback agent once with the identical artifact and instruction.
3. If both attempts fail technically, write `BLOCKED` with both errors and
   stop. Do not try other models or consume quota in a loop.
4. If the agent returns an architectural `BLOCKED`, test failure, or review
   `REJECT`, that is a workflow result, not a model failure. Follow the handoff
   path instead of switching models.
5. Allow no more than one CSA-authorized remediation cycle per work order.
   A second rejection or block requires an owner decision.

## Parent Conversation Launch Instruction

Start an OpenHands conversation on the QAOS branch with a concrete objective,
then give it the following instruction:

```text
Act only as the QAOS Builder Chain orchestrator. Read AGENTS.md and
docs/control-plane/OPENHANDS_BUILDER_CHAIN.md. For the stated objective,
delegate sequentially to qaos-csa, qaos-principal-engineer, and qaos-reviewer.
Require the named package artifact at every handoff. Use a stage's fallback
agent only for a technical delegation/model execution error, once, and record
the error. Never treat VERIFIED as VALIDATED or DESIGNATED. Never allow a
sub-agent to exceed its role. Stop after ACCEPT, or after the defined block or
remediation limit. Report the final work-order ID, review verdict, changed
files, exact verification results, and next owner action.
```

## Cloud Prerequisites

- Sub-agent delegation must remain enabled in OpenHands Agent settings.
- Turn on the OpenHands Critic as an additional guard when the signed-in Cloud
  settings session is available. Critic output is advisory and does not replace
  `qaos-reviewer`.
- The parent Cloud LLM profile must be selected and tested before a smoke run.
- This inherited-model configuration is a temporary orchestration proof. A
  controlled SDK or Agent Server profile store is required before QAOS can
  claim independent role models or ordered model-level fallback.
