# WO-132 — Publication Primitive Gate

2026-09-04; baseline 5e5f0f8; feat/operational-builder-chain.
Authority: OWNER-DECISION-027 and owner request to proceed.
Scope: Windows-only os.rename directory probe and evidence records, no product
code. Test same-volume success, empty/nonempty directory and file collision,
and 20 synchronized two-process publisher races. Verify complete winner and
unchanged losing source, existing destination hashes/timestamps, cleanup and
active data. Stop after gate result; no project implementation in this work order.
Only disposable owned descendants of a unique repository-local temporary root
may be moved or removed. No settings/provider/credential or unrelated changes.

Complete: gate passed on local C: NTFS, Windows 11 build 22631, Python 3.14.3.
See VERIFICATION-110 and HANDOFF-112. Product implementation remains separate.
