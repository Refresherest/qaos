# Authority and Reconciliation

## Authority order

1. The repository owner makes product, risk, and architectural decisions.
2. Accepted ADRs in `docs/architecture/adr/` govern their stated scope.
3. Version-controlled implementation and reproducible tests establish what
   the software currently does.
4. Version-controlled control-plane records establish current work state.
5. Untracked files, prior reports, chat transcripts, tickets, and tool output
   are evidence only until recorded and reconciled.

Higher authority resolves conflicts. A lower item never silently overrides a
higher one. The untracked architecture ADRs/reports present at the Stage 9
baseline are expressly classified as drafts/evidence, not accepted ADRs. When
their claims conflict with code or one another, record evidence and obtain a
new owner decision before treating a claim as a governing rule.

## Reconciliation procedure

1. Create a `CONTRADICTION-###` record from the template.
2. Quote the exact paths, line ranges, commit or working-tree status, and
   reproduction command for each side.
3. Classify it as `documentation-conflict`, `implementation-violation`,
   `stale-report`, or `unknown`.
4. Link the governing ADR(s), affected findings, and proposed options.
5. Obtain an owner decision. Record whether the decision changes code, an ADR,
   a report, or no artifact.
6. Verify the resolution and link it from `PROJECT_STATE.json`.

An inspector result is a finding, not authority to refactor. `REVIEW` means
evidence is insufficient for an automated conclusion.

## Baseline integrity

Every baseline must record: Git commit, branch, dirty/untracked state, Python
command, timestamp, tool version, and source paths inspected. A baseline is
invalidated by a relevant source, ADR, or tool change and must be rerun.
