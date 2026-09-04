# VERIFICATION-111 — WO-133

2026-09-04, baseline 9f3d93a. Outcome: ACCEPT WITH NOTES.

Added python_project v1 intent and separate empty-default project permissions/
workspace, exact four-file trusted source and project capability. Integrated
through existing session, factory, PlannerManager, Task, resolver and Executive
recovery authority. Existing file/template source and intent contracts preserved.
No new orchestration or domain storage. CLI verifier reuses fixed cases with
project-only environment isolation/bytecode suppression flags.

Verification using .venv/Scripts/python.exe:

- Compatibility suite (trusted text/CLI templates and factory opt-in): 37 passed.
- Initial project-focused suite: 25 passed before added edge cases.
- Fresh-process public build/discovery test: 1 passed independently.
- Final `-m pytest -q -p no:cacheprovider --basetemp C:/Projects/qaos/.wo133-final-tmp`:
  285 passed in 65.82s. Active-data SHA256 hashes/timestamps unchanged.
- `-m compileall -q src tests`: passed.
- pkgutil/import sweep: 194 QAOS modules imported.
- `tools/architecture_inspect.py`: 196 source files; pre-existing duplicate,
  registry and singleton findings remain outside scope. Whitespace checks pass.

Coverage: public four-file generation/digests/serialization; fresh-process build
and read-only discovery; standalone app use; fixed cross-file tests plus 15 CLI
cases; corrupt CLI rejection independent of passing generated self-tests;
missing/corrupt/extra members; invalid names/versions/fields; existing targets;
workspace isolation; no project authority from old permissions; disabled recovery
without writes; pre-publication cleanup and explicit recovery when target absent;
cleanup failure and unknown-member retention; changed staging identity refusal;
injected publication race; post-publication failure/refusal; interruption after
rename recorded as uncertain publication while output remains preserved.

Platform guard rejects non-Windows, non-fixed/non-NTFS volumes and reparse
ancestors. Reparse-flag test is simulated, not a live hostile-junction race.
Runtime volume detection uses documented read-only Windows APIs:
https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-getvolumeinformationw
https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-getdrivetypew
No support claimed outside local Windows/NTFS. Publication primitive's 20 actual
two-process races are WO-132 evidence; this work injects a collision at the
capability boundary. Each verification child has a five-second timeout; a build
has 17 verification children, not a five-second overall deadline.

Cleanup only unlinks known flat members after root/reparse/inode ownership checks.
Unexpected files or cleanup failures retain the owned stage and record its
relative name; never scan/delete abandoned stages. Published output is never
cleanup scope. No transaction across rename and execution-state persistence;
existing-output recovery refuses, including matching output. No guarantees for
power loss or hostile concurrent filesystem modification.

Same-agent Reviewer checklist, not independent review. Architecture-awareness
kept project output distinct while reusing existing lifecycle owners. No provider,
credential, active migration, UI or unrelated changes. No new blocker found;
limitations above remain explicit. All temporary test directories are untracked.
