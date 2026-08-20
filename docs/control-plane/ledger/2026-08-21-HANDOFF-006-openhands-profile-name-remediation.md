# HANDOFF-006: OpenHands Named Profile Remediation

- Status: ready for repeat Cloud validation
- Work order: WO-015
- Date: 2026-08-21

## Finding

The initial no-code Cloud smoke test proved that OpenHands discovered and
attempted to delegate to `qaos-csa`. It then stopped correctly because the
agent used raw model IDs, while Cloud requires exact named LLM-profile values
in file-based agent frontmatter.

## Remediation

- Replaced raw IDs with the exact Cloud profile names in all six agent files.
- Replaced the unusable `OpenHands / glm-5.2` fallback route with named
  compatible-profile candidates.
- Preserved the bounded one-primary, one-fallback policy.
- Did not add credentials or designate QAOS models.

## Required Repeat Validation

Run the same `SMOKE-001` no-code workflow. Success requires the parent to
delegate through CSA, PE, and Reviewer and return the Reviewer's verdict with
no repository changes.
