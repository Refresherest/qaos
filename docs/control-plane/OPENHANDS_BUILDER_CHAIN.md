# QAOS OpenHands Builder Chain

## Operational Roles

The project defines six OpenHands file-based sub-agents in `.agents/agents/`:

| Stage | Primary agent | Candidate model profile | Technical fallback agent | Candidate model profile |
| --- | --- | --- | --- | --- |
| Architecture | `qaos-csa` | `QAOS-Deepseek-v4-pro-0813` | `qaos-csa-fallback` | `QAOS-QwenCoderPlus` |
| Implementation | `qaos-principal-engineer` | `QAOS-QwenCoderNext` | `qaos-principal-engineer-fallback` | `QAOS-QwenCoderNext` |
| Independent review | `qaos-reviewer` | `QAOS-Deepseek-v3.2` | `qaos-reviewer-fallback` | `QAOS-KimiK27Code` |

These are exact OpenHands Cloud profile names and transport-verified model
candidates, not QAOS `VALIDATED` or `DESIGNATED` model assignments. The
fallback profiles are used only for a
technical agent/model execution failure (for example provider error,
authentication error, timeout, or malformed tool response), not for a hard
problem, disagreement, failed test, or an architectural block.

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
- The named Cloud LLM profiles must exist and be tested through one complete
  builder-chain run before this setup can be described as operationally proven.
- OpenHands Cloud currently exposes individual profiles, not a native ordered
  provider-failover field. The bounded retry policy above is therefore the
  explicit QAOS fallback mechanism.
