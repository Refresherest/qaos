"""Fixed repository-owned CLI cases, never caller-supplied commands."""

import json
import subprocess
import sys
import tempfile

# Expected counts are literal acceptance values independent of implementation.
CASES = (
    (("--text", "hello world"), (11, 2, 1)),
    (("--text", ""), (0, 0, 0)),
    (("--text=",), (0, 0, 0)),
    (("--text", "one\ntwo"), (7, 2, 2)),
    (("--text", "猫 café"), (6, 2, 1)),
    (("--text=-dash",), (5, 1, 1)),
    (("--text", "x" * 4096), (4096, 1, 1)),
    (("--text", "猫" * 4096), (4096, 1, 1)),
    (("--text", "x" * 4097), None),
    (("--text",), None),
    (("--unknown",), None),
    (("--text", "a", "--text", "b"), None),
    (("--text=a", "--text=b"), None),
    (("--text", "-dash"), None),
    (("--text=a", "extra"), None),
)


def verify(target, timeout, evidence):
    evidence["cli_cases_passed"] = 0
    for index, (arguments, counts) in enumerate(CASES):
        with tempfile.TemporaryFile() as out, tempfile.TemporaryFile() as err:
            result = subprocess.run(
                [sys.executable, str(target), *arguments], cwd=target.parent,
                stdin=subprocess.DEVNULL, stdout=out, stderr=err,
                timeout=timeout, shell=False,
            )
            out.seek(0)
            err.seek(0)
            stdout, stderr = out.read(4097), err.read(4097)
        expected = b""
        if counts is not None:
            expected = (json.dumps(dict(zip(("characters", "words", "lines"), counts)),
                                   sort_keys=True) + "\n").encode("ascii")
        expected_error = b"Invalid text arguments\n" if counts is None else b""
        if (result.returncode != (2 if counts is None else 0)
                or stdout.replace(b"\r\n", b"\n") != expected
                or stderr.replace(b"\r\n", b"\n") != expected_error):
            raise RuntimeError(f"trusted CLI acceptance failed at case {index + 1}")
        evidence["cli_cases_passed"] += 1
