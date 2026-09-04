# VERIFICATION-110 — WO-132

2026-09-04; baseline 5e5f0f8. Outcome: ACCEPT WITH NOTES.

Candidate: Windows os.rename, directly invoked without existence precheck,
replacement flags or fallback. Python documents Windows existing-target refusal:
https://docs.python.org/3/library/os.html#os.rename
This platform-specific rule must not be generalized to POSIX rename semantics.

`.venv/Scripts/python.exe docs/control-plane/ledger/wo132_publication_probe.py`
passed on Windows-11-10.0.22631-SP0, Python 3.14.3, local C: fixed NTFS volume.
Get-Volume initially required read escalation; the approved read confirmed NTFS.
All fixtures were under a unique repository-local owned disposable directory.

- Success preserved all four member hashes/timestamps and removed source name.
- Existing empty directory, nonempty directory and file each raised
  FileExistsError, WinError 183. Source and destination content/timestamps preserved.
- Twenty synchronized two-process races each produced exactly one publisher
  and one refusal. Winner had all four expected files; losing source unchanged.
- Temporary root removed after confinement validation; active data unchanged.
- `-m py_compile docs/control-plane/ledger/wo132_publication_probe.py` passed.

This is the bounded prerequisite gate for the tested local platform, not formal
proof under every concurrent observer or filesystem failure. No power-loss,
hostile mutation, reparse-point attack, cross-volume, network filesystem or
cross-platform guarantee. Implementation must still enforce approved confinement,
reparse rejection, exact members, lifecycle and crash-gap recovery contracts.
Unsupported platforms must fail closed; no copy/replace fallback authorized.

Only probe/records changed. Architecture-awareness kept the gate separate from
product generation; same-agent review, not independent delegation. Full tests,
import sweep and architecture inspection were not rerun for this isolated
filesystem probe. Last full regression remains WO-129's 253 passing tests.
Unrelated modified skills/untracked material and providers/credentials untouched.
