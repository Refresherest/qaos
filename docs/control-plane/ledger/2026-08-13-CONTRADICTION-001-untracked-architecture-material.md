# CONTRADICTION-001: Architecture material exists outside version control

- Status: resolved
- Conflicting sources: committed `v0.1.0-executive-baseline` versus untracked
  `docs/architecture/` ADRs/reports and `docs/vision/`.
- Classification: documentation-conflict / provenance gap

## Evidence

`git status --short` shows the architecture materials as untracked. Their
content is useful evidence and is referenced by this control plane, but they
cannot be assumed accepted or historically tied to the baseline commit.

## Owner decision

Retain the material as drafts/evidence only. It may contain correct portions,
but it was produced under prior CSA direction that may have suffered memory loss
or hallucination. QAOS is in core-architecture recovery: new contracts derive
from executable evidence and fresh owner-approved decisions, not these drafts.
