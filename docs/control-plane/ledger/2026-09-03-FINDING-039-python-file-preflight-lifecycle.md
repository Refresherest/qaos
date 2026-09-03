# FINDING-039 — Python-File Target Rejection Leaves Task Pending

Status: RESOLVED in WO-120 after explicit owner scope-extension approval.
Original reproduction baseline: b030801 plus local WO-120 draft.

Reproduction:
`.venv\Scripts\python.exe -m pytest tests/test_application_intent_submission.py -q -p no:cacheprovider --basetemp C:/Projects/qaos/.wo120-focused-tmp`

Observed: 7 passed, 1 failed. Existing output file raises FileExistsError.
Objective and QueueItem fail, but persisted Plan Task remains pending.
Failing test: test_existing_output_failure_preserves_truthful_task_state.

Cause: PythonFileCapability.execute invokes _target before task.start and
before its try/except. Target rejection therefore bypasses task failure handling.
DefaultWorker only fails an action already running. This also affects the
Task state when no-overwrite recovery encounters the existing file.

This is an existing capability lifecycle gap exposed by the public-session
path, not authorization to change recovery or overwrite output files.

Proposed narrow extension: move target validation inside the capability's
started Task failure-handling region, retaining no-write/no-overwrite rejection
and the original exception. Update focused capability expectations to require
failed Task state after a valid intent reaches execution but its target is
rejected. Add public-session and recovery coherence assertions.

The owner approved extending WO-120 scope to capabilities/python_file.py and
its focused tests for this lifecycle fix only. No new executable authority.

Resolution: _target now runs after task.start inside the capability's existing
failure-handling region. Rejection preserves the original exception and the
existing file while setting Task failed. Public-session and reloaded recovery
checks prove consistent Plan Task, Queue action/item and Objective failure.
See VERIFICATION-104: 223 tests passed, compile/import checks passed.
