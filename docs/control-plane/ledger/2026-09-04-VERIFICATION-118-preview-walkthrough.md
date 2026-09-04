# VERIFICATION-118 — WO-146 Operator Preview Walkthrough

2026-09-04; baseline a7933f8; Python 3.14.3, local Windows/NTFS.
Verification-only complete; same-agent checks, not independent delegation.

## Repeat the disposable walkthrough

From C:/Projects/qaos in PowerShell:

```powershell
.venv/Scripts/python.exe docs/control-plane/ledger/wo146_preview_walkthrough.py
```

The probe creates uniquely owned state/output directories, launches ten fresh
processes with -B, asserts results and removes its temporary workspace. It reuses
WO-121 fingerprints. No app remains afterward. Do not run assertion-based probes
with Python -O. Active repository data is fingerprinted, not selected for builds.

## Operator example

```powershell
.venv/Scripts/python.exe -B -m qaos.main preview-project --directory Example --brief "count words and lines"
```

Read the JSON: status is preview, grammar_version is 1, template is
text_stats_project_v2 and metrics are [words,lines]. There is no objective ID
because nothing was built or persisted. The directory is validated as a name,
not inspected on disk. The same preview results from `  Count LINES  and words  `.

Supported grammar is count followed by one to three distinct metrics from
characters/words/lines joined by and. ASCII case and ordinary spaces may vary;
the whole brief must fit 1–256 ASCII letters/spaces. Not free-form language.
`count words and publish it` and `count words and words` are rejected in full,
not partially interpreted. Permission flags on preview are also rejected.

After reviewing, a build is a separate explicit operator action:

```text
python -m qaos.main build-project --workspace <state> --output-root <output> --directory Example --metrics words,lines --enable-project text_stats_project_v2
```

Replace placeholders with existing, absolute, non-overlapping directories; quote
paths containing spaces. Existing Windows/NTFS and reparse safeguards apply.
The probe supplies a fixed separate build request; it does not load/execute preview
JSON. A preview cannot authorize a build, choose roots or bypass collisions.
Review unsupported wording rather than assuming omitted clauses were understood.

## Observed results

| Phase | Exit | Result |
| --- | --- | --- |
| Preview | 0 | Exact v1 preview envelope and v2 intent. |
| Case/space variant | 0 | Identical normalized preview. |
| Unsupported clause | 2 | Static diagnostic, empty stdout. |
| Duplicate metric | 2 | Same refusal contract. |
| Permission flag on preview | 2 | Refused; no execution authority. |
| Build without permission | 2 | Preview does not grant permission. |
| Separate authorized build | 0 | Persisted intent equals preview intent. |
| Standalone app | 0 | Multiline input yields words=3, lines=2. |
| Discovery | 0 | Completed objective found without writes. |
| Collision | 1 | FileExistsError; successful records/output preserved. |

Preview and refusal phases leave state/output empty and no extra directory or
objective. Standalone/discovery do not mutate records. Collision does not replace
output or leave residual staging. The probe preserves active-data hashes/timestamps
and removes its owned temporary workspace. This is not a general sandbox claim.

Verification using .venv/Scripts/python.exe:

- `docs/control-plane/ledger/wo146_preview_walkthrough.py`: all ten phases pass,
  exit codes [0,0,2,2,2,2,0,0,0,1].
- `-m pytest tests/test_controlled_preview.py tests/test_build_project_cli.py -q
  -p no:cacheprovider --basetemp C:/Projects/qaos/.wo146-focused-tmp`:
  143 passed in 17.31s.
- `-m py_compile docs/control-plane/ledger/wo146_preview_walkthrough.py`: passed.

No product or existing tests changed, so full 450-test, 198-import and architecture
results remain WO-145 evidence, not rerun here. JSON/whitespace checks validate
records. Engineering guidance kept this within public-command verification and
existing helper contracts. Unrelated dirty skills/untracked configuration/drafts/
tools/test folders preserved; new focused artifacts left untracked. No credentials,
providers, models, OpenHands or permission/grammar expansion.
