"""Bounded execution of the approved deterministic Python-file intent."""

import hashlib
import os
from pathlib import Path, PurePath
import subprocess
import sys
import tempfile

from qaos.planner.intents import PythonFileIntent


class PythonFileCapability:
    name = "python_file"

    def __init__(self, workspace, *, timeout_seconds=5):
        workspace = Path(workspace)
        if not workspace.is_dir():
            raise ValueError("workspace must be an existing directory")
        if not isinstance(timeout_seconds, int) or not 1 <= timeout_seconds <= 30:
            raise ValueError("timeout_seconds must be an integer from 1 through 30")
        self._workspace = workspace.resolve(strict=True)
        self._timeout = timeout_seconds

    def execute(self, item):
        task = item.action
        intent = getattr(task, "intent", None)
        if not isinstance(intent, PythonFileIntent):
            raise TypeError("python_file capability requires PythonFileIntent")

        task.start()
        try:
            target = self._target(intent.relative_path)
            self._atomic_create(target, intent.source.encode("utf-8"))
            with tempfile.TemporaryFile() as stdout_file, tempfile.TemporaryFile() as stderr_file:
                completed = subprocess.run(
                    [sys.executable, str(target)], cwd=self._workspace,
                    stdin=subprocess.DEVNULL, stdout=stdout_file, stderr=stderr_file,
                    timeout=self._timeout, shell=False,
                )
                stdout_file.seek(0)
                stderr_file.seek(0)
                stdout_bytes = stdout_file.read(4097)
                stderr_bytes = stderr_file.read(4097)
            stdout = self._normalized_text(stdout_bytes[:4096])
            stderr = self._normalized_text(stderr_bytes[:4096])
            evidence = {
                "intent_type": intent.type,
                "intent_version": intent.version,
                "relative_path": intent.relative_path,
                "source_sha256": hashlib.sha256(intent.source.encode("utf-8")).hexdigest(),
                "verifier": "current_python_direct",
                "exit_code": completed.returncode,
                "stdout": stdout,
                "stderr": stderr,
                "output_truncated": len(stdout_bytes) > 4096 or len(stderr_bytes) > 4096,
            }
            item.result = evidence
            if completed.returncode != 0 or stdout != intent.expected_stdout:
                raise RuntimeError("python file verification failed")
        except Exception:
            if task.status == "running":
                task.fail()
            raise
        task.complete()
        return evidence

    def _target(self, relative_path):
        candidate = PurePath(relative_path)
        if candidate.is_absolute() or ".." in candidate.parts:
            raise ValueError("target must be a workspace-relative path")
        if candidate.suffix != ".py" or candidate.name in {"", ".", ".."}:
            raise ValueError("target must be a .py file")
        target = self._workspace.joinpath(*candidate.parts)
        if not target.parent.is_dir():
            raise ValueError("target parent must already exist")
        parent = target.parent.resolve(strict=True)
        if parent != self._workspace and self._workspace not in parent.parents:
            raise ValueError("target escapes the workspace")
        if target.exists() or target.is_symlink():
            raise FileExistsError("target already exists")
        return target

    @staticmethod
    def _atomic_create(target, content):
        temporary_path = None
        try:
            with tempfile.NamedTemporaryFile(dir=target.parent, delete=False) as temporary:
                temporary_path = Path(temporary.name)
                temporary.write(content)
                temporary.flush()
                os.fsync(temporary.fileno())
            os.link(temporary_path, target)
        finally:
            if temporary_path is not None:
                temporary_path.unlink(missing_ok=True)

    @staticmethod
    def _normalized_text(content):
        return content.decode("utf-8", errors="replace").replace("\r\n", "\n").replace("\r", "\n")
