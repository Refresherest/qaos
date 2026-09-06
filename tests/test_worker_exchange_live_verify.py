import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

TOOLS = Path(__file__).parents[1] / "tools" / "qaos-worker"
sys.path.insert(0, str(TOOLS))
import qaos_worker_live_verify as live_verify


def test_pre_correlation_rejection_requires_exact_remote_status(monkeypatch):
    monkeypatch.setattr(
        live_verify,
        "ssh_exchange",
        lambda *args: SimpleNamespace(returncode=1, stdout=b""),
    )
    request, _ = live_verify.build_probe()
    live_verify.expect_pre_correlation_rejection("host", "key", "known", request)


def test_pre_correlation_rejection_excludes_ssh_transport_failure(monkeypatch):
    monkeypatch.setattr(
        live_verify,
        "ssh_exchange",
        lambda *args: SimpleNamespace(returncode=255, stdout=b""),
    )
    request, _ = live_verify.build_probe()
    with pytest.raises(RuntimeError, match="silent pre-correlation rejection"):
        live_verify.expect_pre_correlation_rejection("host", "key", "known", request)
