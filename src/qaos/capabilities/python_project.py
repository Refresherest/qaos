"""Opt-in local Windows/NTFS trusted-project publication, no overwrite/adoption."""
import ctypes
from ctypes import wintypes
import hashlib
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile

from qaos.planner.intents import PythonProjectIntent, project_allowlist
from .text_stats_project import MEMBERS
from .text_stats_cli_verifier import verify as verify_cli
from .text_stats_cli_template import SUCCESS_MARKER


def reject_reparse(path):
    for entry in (path, *path.parents):
        info = entry.lstat()
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
            raise ValueError("project path contains a reparse point")


def require_local_ntfs(path):
    if sys.platform != "win32":
        raise RuntimeError("project publication supports local Windows NTFS only")
    reject_reparse(path)
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    drive = kernel.GetDriveTypeW
    drive.argtypes, drive.restype = [wintypes.LPCWSTR], wintypes.UINT
    volume = kernel.GetVolumeInformationW
    volume.argtypes = [wintypes.LPCWSTR, wintypes.LPWSTR, wintypes.DWORD,
                       ctypes.POINTER(wintypes.DWORD), ctypes.POINTER(wintypes.DWORD),
                       ctypes.POINTER(wintypes.DWORD), wintypes.LPWSTR, wintypes.DWORD]
    volume.restype = wintypes.BOOL
    fs = ctypes.create_unicode_buffer(64)
    if drive(path.anchor) != 3 or not volume(path.anchor, None, 0, None, None, None, fs, 64):
        raise RuntimeError("project filesystem support could not be verified")
    if fs.value != "NTFS":
        raise RuntimeError("project publication supports local Windows NTFS only")


class PythonProjectCapability:
    name = "python_project"

    def __init__(self, workspace, *, enabled_python_projects=()):
        self._enabled = project_allowlist(enabled_python_projects)
        path = Path(workspace)
        if not path.is_absolute() or not path.is_dir():
            raise ValueError("project workspace must be an existing absolute directory")
        require_local_ntfs(path)
        self._workspace = path.resolve(strict=True)

    def _check_root(self):
        require_local_ntfs(self._workspace)

    def _populate(self, stage):
        for name, source in MEMBERS.items():
            with (stage / name).open("xb") as stream:
                stream.write(source.encode("utf-8"))
                stream.flush()
                os.fsync(stream.fileno())

    def _check_members(self, directory):
        reject_reparse(directory)
        if {p.name for p in directory.iterdir()} != set(MEMBERS):
            raise RuntimeError("project member set differs from trusted template")
        hashes = {}
        for name in sorted(MEMBERS):
            member = directory / name
            reject_reparse(member)
            if not member.is_file() or member.read_bytes() != MEMBERS[name].encode("utf-8"):
                raise RuntimeError("project member differs from trusted template")
            hashes[name] = hashlib.sha256(member.read_bytes()).hexdigest()
        return hashes

    @staticmethod
    def _run_fixed(target, marker):
        with tempfile.TemporaryFile() as out, tempfile.TemporaryFile() as err:
            result = subprocess.run([sys.executable, "-E", "-s", "-B", str(target)],
                                    cwd=target.parent, stdin=subprocess.DEVNULL,
                                    stdout=out, stderr=err, shell=False, timeout=5)
            out.seek(0)
            err.seek(0)
            if (result.returncode != 0 or out.read(4097).replace(b"\r\n", b"\n") != marker
                    or err.read(4097) != b""):
                raise RuntimeError("project fixed verification failed")

    def _verify(self, stage, evidence):
        self._run_fixed(stage / "test_stats.py", b"QAOS project tests PASS\n")
        self._run_fixed(stage / "app.py", SUCCESS_MARKER.encode("ascii"))
        verify_cli(stage / "app.py", 5, evidence, project_mode=True)

    def _publish(self, stage, target):
        self._check_root()
        reject_reparse(stage)
        if stage.parent != self._workspace or target.parent != self._workspace:
            raise ValueError("publication outside owned root")
        os.rename(stage, target)  # Windows no-replace; never os.replace or copy fallback.

    def _cleanup(self, stage, identity):
        self._check_root()
        reject_reparse(stage)
        if stage.parent != self._workspace or stage.stat().st_ino != identity:
            raise RuntimeError("staging ownership could not be verified")
        # Only flat, known members created by this template. Unexpected content
        # is retained for explicit inspection, not recursively deleted.
        children = list(stage.iterdir())
        for child in children:
            reject_reparse(child)
            if child.name not in MEMBERS or not child.is_file():
                raise RuntimeError("unexpected staging content; cleanup refused")
        for child in children:
            child.unlink()
        stage.rmdir()

    def execute(self, item):
        task, stage, identity = item.action, None, None
        intent = task.intent
        if type(intent) is not PythonProjectIntent:
            raise TypeError("project capability requires PythonProjectIntent")
        PythonProjectIntent.from_dict(intent.to_dict())
        if intent.template_id not in self._enabled:
            raise ValueError("project template is not enabled")
        evidence = {"intent_type": intent.type, "intent_version": 1,
                    "template_id": intent.template_id, "template_version": 1,
                    "relative_directory": intent.relative_directory,
                    "verifier": "trusted_project_cases_v1", "published": False}
        item.result = evidence
        task.start()
        try:
            self._check_root()
            target = self._workspace / intent.relative_directory
            if os.path.lexists(target):
                raise FileExistsError("project destination already exists; adoption refused")
            stage = Path(tempfile.mkdtemp(prefix=".qaos-stage-", dir=self._workspace))
            identity = stage.stat().st_ino
            self._populate(stage)
            self._check_members(stage)
            self._verify(stage, evidence)
            evidence["member_sha256"] = self._check_members(stage)
            self._publish(stage, target)
            evidence["published"] = True
            stage = None  # Published data is never cleanup scope, even on later failure.
            if self._check_members(target) != evidence["member_sha256"]:
                raise RuntimeError("published project integrity mismatch")
            task.complete()
            return evidence
        except Exception as error:
            if task.status == "running":
                task.fail()
            if stage is not None and not os.path.lexists(stage):
                evidence["publication_uncertain"] = True
                # An interruption around rename must not be reported as a
                # confirmed unpublished attempt or trigger target cleanup.
                evidence["published"] = None
            if stage is not None and os.path.lexists(stage):
                evidence["residual_stage"] = stage.name
                try:
                    self._cleanup(stage, identity)
                    evidence.pop("residual_stage")
                except Exception as cleanup_error:
                    evidence["cleanup_error"] = type(cleanup_error).__name__
                    raise RuntimeError("project failed; staging cleanup failed; inspect residual_stage") from error
            raise
