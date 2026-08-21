# WO-016: OpenHands Verified Primary Profile Remediation

- Status: ready-for-cloud-validation
- Owner: Qaasim April
- Executor: QAOS Principal Engineer
- Authority: Owner-approved continuation of the no-code builder-chain smoke test; `AGENTS.md`; WO-015 runtime evidence.
- Objective: Replace the three OpenHands Builder Chain primary-agent profile references with exact Cloud profile names that have each returned `PROFILE TEST OK` in OpenHands.
- Scope: Update only the three primary agent `model` fields, the matching primary entries in `docs/control-plane/OPENHANDS_BUILDER_CHAIN.md`, and this ledger record.
- Non-goals: Modify QAOS product code; add or change credentials; designate models; change Cloud profiles; use OpenRouter; alter fallback assignments; run product work.

## Verification Evidence

The owner verified basic OpenHands responses for these exact named profiles:

| Builder stage | Primary profile | Evidence state |
| --- | --- | --- |
| CSA | `QAOS-Deepseek-v4-pro-0813` | `PROFILE TEST OK` |
| PE | `QAOS-QwenCoderNext` | `PROFILE TEST OK` |
| Reviewer | `QAOS-Deepseek-v3.2` | `PROFILE TEST OK` |

This is transport evidence only. It does not constitute QAOS model
`VALIDATED` or `DESIGNATED` status.

## Approved Primary Mapping

| Agent | Cloud profile name |
| --- | --- |
| `qaos-csa` | `QAOS-Deepseek-v4-pro-0813` |
| `qaos-principal-engineer` | `QAOS-QwenCoderNext` |
| `qaos-reviewer` | `QAOS-Deepseek-v3.2` |

The existing fallback assignments are intentionally unchanged because they
have not been retested in the current Cloud configuration. OpenRouter is
explicitly excluded from this work order.

## Acceptance Criteria

1. Each primary agent references its exact owner-tested Cloud profile name.
2. The protocol table matches the primary agent files.
3. No credentials, model designations, or OpenRouter references are added.
4. A repeat no-code Cloud smoke test reaches all three primary roles or records a new bounded runtime finding.

## Stop Condition

Stop after publishing the mapping and rerunning the no-code smoke test. Do not start QAOS product work.
