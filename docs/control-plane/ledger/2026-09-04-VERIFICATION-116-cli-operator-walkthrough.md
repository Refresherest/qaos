# VERIFICATION-116 — WO-142 Operator Walkthrough

2026-09-04; baseline d2efdcc; Windows/local NTFS; Python 3.14.3.
Completed verification-only walkthrough; same-agent checks, not independent review.

## Reproduce safely

From C:/Projects/qaos in PowerShell:

```powershell
.venv/Scripts/python.exe docs/control-plane/ledger/wo142_cli_walkthrough.py
```

This creates uniquely named temporary state/output folders under the repository,
runs nine fresh CLI/application subprocesses, checks results and removes only
its owned temporary workspace. It does not leave a usable app behind. The public
commands are executed from that workspace with an explicit src PYTHONPATH; the
standalone generated app uses -E -s -B and does not depend on QAOS imports.
Do not run the assertion-based verification script with Python optimization (-O).

## Manual operator sequence

Choose two existing, absolute, separate folders: one for QAOS records, one for
generated projects. They must not overlap or traverse reparse points; output
must be local Windows NTFS. Replace every placeholder below before use; these
examples do not create directories or select active repository data for you.
Use an installed QAOS environment or the repository's configured virtualenv.

```text
python -m qaos.main build-project --workspace <state> --output-root <output> --directory Example --metrics lines,words --enable-project text_stats_project_v2
python -E -s -B <output>/Example/app.py --text "one two three"
python -E -s -B <output>/Example/test_stats.py
python -m qaos.main objectives --workspace <state>
```

Quote paths containing spaces. The build prints an objective ID, completion,
published directory and normalized metrics words,lines. The one-line manual
text example returns words=3, lines=1. The executed probe instead passes a newline
between two and three and verifies words=3, lines=2. Exactly four files publish:
stats.py, app.py, test_stats.py and README.md. Generated tests print
`QAOS project tests PASS`. Runtime logs mean build output is not JSON-only.

## Observed outcomes and operator response

| Phase | Exit | Meaning / response |
| --- | --- | --- |
| Missing permission | 2 | Usage error; supply the explicit v2 opt-in only if intended. |
| Missing state directory | 1 | ValueError; choose an existing absolute state root. |
| Overlapping roots | 1 | ValueError; choose separate non-nested roots. |
| Build | 0 | Completed; retain objective ID and output location. |
| Standalone app | 0 | Exact selected output: words=3, lines=2. |
| Generated tests | 0 | Fixed success marker verified. |
| Objective discovery | 0 | Completed objective found without writes. |
| Same-directory build | 1 | FileExistsError; inspect existing project, do not overwrite. |
| Default recovery | 1 | ValueError; this command does not grant project permission. |

A collision creates a distinct failed objective with coherent plan/queue status;
the original successful records and output remain unchanged. Keep the printed
failed objective ID for diagnostics. Do not use recovery as a permission bypass.
If a separate new build is intended, choose a new unused directory name explicitly;
this walkthrough did not test automatic retries or output editing/adoption.
Early request/root failures occur before objective creation and have no ID.
The adapter reports exception types, not detailed exception payloads.

## Verification record

Using .venv/Scripts/python.exe:

- `docs/control-plane/ledger/wo142_cli_walkthrough.py`: nine phases passed, codes
  [2,1,1,0,0,0,0,1,1]. Four hashes matched evidence; canonical selected metrics,
  read-only early refusals/discovery/default recovery, preserved successful records,
  coherent failed status, no residual stage, active data unchanged, owned workspace removed.
- `-m pytest tests/test_build_project_cli.py tests/test_cli_kernel.py
  tests/test_recovery_cli.py tests/test_objective_discovery_cli.py -q
  -p no:cacheprovider --basetemp C:/Projects/qaos/.wo142-cli-tmp`: 82 passed in 10.06s.
- `-m py_compile docs/control-plane/ledger/wo142_cli_walkthrough.py`: passed.

Full 354-test, 196-import and architecture results remain WO-141 evidence, not
rerun here because no product or existing test code changed. JSON/whitespace
checks validate these records. Existing .pytest_cache warning remains unrelated.
Engineering guidance kept this to public-command verification and reused existing
fingerprint helpers. No credential/provider/model/Content OS changes. Unrelated
dirty skills, untracked configuration/drafts/tools/test folders preserved; new
focused regression artifacts remain untracked. No production-readiness claim.
