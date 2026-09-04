# VERIFICATION-114 — WO-138

2026-09-04; baseline 5111dd6; Windows, Python 3.14.3.
Outcome: ACCEPT WITH NOTES (same-agent checklist, not independent delegation).

Commands use .venv/Scripts/python.exe from C:/Projects/qaos:

- `docs/control-plane/ledger/wo138_configurable_probe.py`: passed, nine fresh
  top-level processes, exit codes [0,0,0,0,1,1,1,1,1]. Expected nonzero codes
  represent collision and authorization refusals, not unexpected test failures.
- `-m pytest -q -p no:cacheprovider --basetemp C:/Projects/qaos/.wo138-full-tmp`:
  307 passed in 157.28s. Active-data hashes and timestamps unchanged across suite.
- `-m py_compile docs/control-plane/ledger/wo138_configurable_probe.py`: passed.
- `-m compileall -q src tests`: passed.
- `tools/architecture_inspect.py`: 197 files, 22 existing findings; not authority
  for unrelated fixes. No product source changed. Import sweep was not rerun.

Probe assertions: unsorted input [lines,words] is saved canonically as
[words,lines] in plan intent and result evidence, with exact v2 template/intent/
verifier identity. Four published files match persisted SHA-256 digests.
Standalone app returns exactly words=3 and lines=2 for one two/newline/three;
generated tests pass. Fresh-process objective discovery sees completed status
without writes. Default, v1-only and workspace-only recovery permissions refuse
without changing state/output. Authorized recovery of a collision refuses rather
than adopting existing output. Failure state remains coherent; original successful
records, bytes and timestamps are preserved. No residual staging appears.
Disposable probe workspace was removed; active data remained unchanged.

Scope review: four new ledger files (work order, probe, verification, handoff)
and two current-state records only. Existing three dirty skill files, untracked
configuration/drafts/tools and prior test directories are preserved and excluded.
New full-suite temporary artifacts remain untracked. No credentials/provider,
OpenHands, product code or existing tests changed; no model readiness claim.
Architecture-awareness reused existing helpers/public contracts, without a new
workflow or storage abstraction. Existing Windows/NTFS and crash-gap limitations
remain. All-seven selection coverage is in regressions, not this one-selection
rehearsal. Known unrelated .pytest_cache access warning was not repaired.
