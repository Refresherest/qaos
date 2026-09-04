"""Windows-only no-replace directory publication gate; disposable fixtures."""
import hashlib
import json
import multiprocessing as mp
import os
from pathlib import Path
import platform
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[3]


def fingerprint(path):
    if path.is_file():
        return (hashlib.sha256(path.read_bytes()).hexdigest(), path.stat().st_mtime_ns)
    return {str(p.relative_to(path)): fingerprint(p) for p in path.rglob("*") if p.is_file()}


def confined(path, root):
    resolved = path.resolve()
    assert resolved != root and resolved.is_relative_to(root)
    return resolved


def publish(source, destination, root):
    # No target-existence precheck and no overwrite/copy fallback.
    os.rename(confined(source, root), confined(destination, root))


def populate(path, label):
    path.mkdir()
    for name in ("stats.py", "app.py", "test_stats.py", "README.md"):
        (path / name).write_text(label + ":" + name, encoding="utf-8")


def contender(source, target, root, barrier, queue):
    try:
        barrier.wait(timeout=15)
        publish(source, target, root)
        queue.put((source.name, "published"))
    except FileExistsError as exc:
        queue.put((source.name, "refused", exc.winerror))


def run():
    assert os.name == "nt", "This gate does not authorize POSIX os.rename"
    active = fingerprint(ROOT / "data")
    with tempfile.TemporaryDirectory(prefix=".wo132-probe-", dir=ROOT) as temporary:
        root = Path(temporary).resolve()
        assert root.parent == ROOT.resolve()
        source, target = root / "source", root / "target"
        populate(source, "success")
        original = fingerprint(source)
        publish(source, target, root)
        assert not source.exists() and fingerprint(target) == original
        errors = []
        for kind in ("empty", "nonempty", "file"):
            src, dst = root / (kind + "-src"), root / (kind + "-dst")
            populate(src, kind)
            if kind == "file":
                dst.write_text("preserve", encoding="utf-8")
            elif kind == "nonempty":
                populate(dst, "existing")
            else:
                dst.mkdir()
            before = (fingerprint(src), fingerprint(dst), dst.stat().st_mtime_ns)
            try:
                publish(src, dst, root)
            except FileExistsError as exc:
                errors.append({"target": kind, "winerror": exc.winerror})
            else:
                raise AssertionError("existing target replaced")
            assert (fingerprint(src), fingerprint(dst), dst.stat().st_mtime_ns) == before
        for index in range(20):
            left, right, dst = (root / f"race-{index}-{suffix}" for suffix in ("a", "b", "dest"))
            populate(left, "left")
            populate(right, "right")
            originals = {p.name: fingerprint(p) for p in (left, right)}
            barrier, queue = mp.Barrier(2), mp.Queue()
            children = [mp.Process(target=contender, args=(p, dst, root, barrier, queue))
                        for p in (left, right)]
            try:
                for child in children:
                    child.start()
                results = [queue.get(timeout=20) for _ in children]
                for child in children:
                    child.join(timeout=5)
                    assert child.exitcode == 0
                winner = [r[0] for r in results if r[1] == "published"]
                loser = [r[0] for r in results if r[1] == "refused"]
                assert len(winner) == len(loser) == 1
                assert fingerprint(dst) == originals[winner[0]]
                assert not (root / winner[0]).exists()
                assert fingerprint(root / loser[0]) == originals[loser[0]]
            finally:
                for child in children:
                    if child.is_alive():
                        child.terminate()
                        child.join(timeout=5)
                queue.close()
                queue.join_thread()
        # TemporaryDirectory cleanup is limited to the validated owned root.
        assert root.parent == ROOT.resolve() and not root.is_symlink()
    assert not root.exists() and fingerprint(ROOT / "data") == active
    print(json.dumps({"platform": platform.platform(), "python": sys.version.split()[0],
                      "primitive": "Windows os.rename", "collision_errors": errors,
                      "races_passed": 20, "winner_complete_loser_preserved": True,
                      "temporary_root_removed": True, "active_data_unchanged": True}, indent=2))


if __name__ == "__main__":
    run()
