#!/usr/bin/env python3
"""Controller-side synthetic probe for the restricted QAOS worker broker."""

from __future__ import annotations

import argparse
import base64
import hashlib
import os
import subprocess
import sys
import uuid
from datetime import datetime, timedelta, timezone

from qaos_worker_broker import (
    IMAGE_DIGEST, LAUNCHER_SHA256, POLICY_ID, RESPONSE_LIMIT,
)
from qaos_worker_exchange import (
    MEMBER_LIMIT, PROTOCOL, REQUEST_LIMIT, VERSION, canonical_json,
    decode_canonical_json, encode_frame, read_frame,
)

RESPONSE_FIELDS = {
    "protocol", "version", "request_id", "nonce", "objective_id", "task_id",
    "candidate_artifact", "acceptance_artifact", "worker_instance_id",
    "launcher_sha256", "runtime_version", "image_digest", "policy_id",
    "started_at", "completed_at", "outcome", "exit_code", "oom_killed",
    "termination_reason", "stdout", "stderr", "resource_evidence",
    "acceptance_results", "cleanup", "response_sha256",
}
WORKER_INSTANCE_ID = "qaos-worker"
RUNTIME_VERSION = "gvisor-20260831.0"
OUTCOMES = {"completed", "candidate_failed", "policy_rejected", "limit_terminated", "runtime_failed", "cleanup_failed"}
STREAM_FIELDS = {"bytes", "sha256", "truncated", "text_preview"}
CLEANUP_FIELDS = {"staging_removed", "launcher_cleanup_reported"}
RESOURCE_FIELDS = {"fixture", "spec_sha256"}
ACCEPTANCE_FIELDS = {"test_id", "status", "duration_ms"}


def timestamp(value):
    return value.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_timestamp(value):
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except (TypeError, ValueError) as error:
        raise ValueError("invalid response timestamp") from error


def is_sha256(value):
    return isinstance(value, str) and len(value) == 64 and all(c in "0123456789abcdef" for c in value)


def build_probe(now=None):
    now = (now or datetime.now(timezone.utc)).replace(microsecond=0)
    members = [
        ("acceptance", "acceptance.txt", b"QAOS synthetic acceptance bytes\n"),
        ("candidate", "candidate.txt", b"QAOS synthetic candidate bytes\n"),
    ]
    manifest = []
    for role, path, payload in members:
        manifest.append({
            "role": role, "path": path, "size": len(payload),
            "sha256": hashlib.sha256(payload).hexdigest(),
        })
    request = {
        "protocol": PROTOCOL, "version": VERSION, "request_id": str(uuid.uuid4()),
        "nonce": base64.urlsafe_b64encode(os.urandom(32)).decode().rstrip("="),
        "created_at": timestamp(now), "expires_at": timestamp(now + timedelta(minutes=2)),
        "objective_id": "synthetic-objective", "task_id": "synthetic-task",
        "candidate_artifact": {"artifact_id": "synthetic-candidate", "content_sha256": manifest[1]["sha256"]},
        "acceptance_artifact": {"artifact_id": "synthetic-acceptance", "content_sha256": manifest[0]["sha256"]},
        "members": manifest,
        "runtime": {"launcher_sha256": LAUNCHER_SHA256, "image_digest": IMAGE_DIGEST, "policy_id": POLICY_ID},
    }
    wire = encode_frame(canonical_json(request), REQUEST_LIMIT)
    for _, _, payload in members:
        wire += encode_frame(payload, MEMBER_LIMIT)
    return request, wire


def validate_response(raw, request):
    import io
    stream = io.BytesIO(raw)
    response = decode_canonical_json(read_frame(stream, RESPONSE_LIMIT))
    if stream.read(1) != b"":
        raise ValueError("trailing response data")
    if set(response) != RESPONSE_FIELDS:
        raise ValueError("invalid response fields")
    for field in ("protocol", "version", "request_id", "nonce", "objective_id", "task_id", "candidate_artifact", "acceptance_artifact"):
        if response[field] != request[field]:
            raise ValueError(f"response correlation mismatch: {field}")
    if response["launcher_sha256"] != LAUNCHER_SHA256 or response["image_digest"] != IMAGE_DIGEST or response["policy_id"] != POLICY_ID:
        raise ValueError("response runtime mismatch")
    if response["runtime_version"] != RUNTIME_VERSION or response["worker_instance_id"] != WORKER_INSTANCE_ID:
        raise ValueError("response worker/runtime identity mismatch")
    if response["outcome"] not in OUTCOMES:
        raise ValueError("invalid response outcome")
    started, completed = parse_timestamp(response["started_at"]), parse_timestamp(response["completed_at"])
    created, expires = parse_timestamp(request["created_at"]), parse_timestamp(request["expires_at"])
    if not (created <= started <= completed and started <= expires):
        raise ValueError("invalid response timestamp order")
    cleanup = response["cleanup"]
    if not isinstance(cleanup, dict) or set(cleanup) != CLEANUP_FIELDS or not all(isinstance(v, bool) for v in cleanup.values()):
        raise ValueError("invalid cleanup evidence")
    for name in ("stdout", "stderr"):
        value = response[name]
        if not isinstance(value, dict) or set(value) != STREAM_FIELDS:
            raise ValueError("invalid stream evidence")
        if not isinstance(value["bytes"], int) or isinstance(value["bytes"], bool) or not 0 <= value["bytes"] <= 1024 * 1024:
            raise ValueError("invalid stream evidence")
        if not is_sha256(value["sha256"]) or not isinstance(value["truncated"], bool) or not isinstance(value["text_preview"], str) or len(value["text_preview"].encode("utf-8")) > 480:
            raise ValueError("invalid stream evidence")
    resource, acceptance = response["resource_evidence"], response["acceptance_results"]
    if not isinstance(resource, dict) or set(resource) != RESOURCE_FIELDS:
        raise ValueError("invalid resource evidence")
    if not isinstance(acceptance, list) or any(not isinstance(v, dict) or set(v) != ACCEPTANCE_FIELDS for v in acceptance):
        raise ValueError("invalid acceptance evidence")
    claimed = response["response_sha256"]
    unsigned = dict(response); unsigned.pop("response_sha256")
    if claimed != hashlib.sha256(canonical_json(unsigned)).hexdigest():
        raise ValueError("response digest mismatch")
    if response["outcome"] == "completed":
        if response["exit_code"] != 0 or response["oom_killed"] is not False or response["termination_reason"] != "completion":
            raise ValueError("invalid completed execution evidence")
        if cleanup != {"staging_removed": True, "launcher_cleanup_reported": True}:
            raise ValueError("completed response requires confirmed cleanup")
        if resource.get("fixture") != "harmless" or not is_sha256(resource.get("spec_sha256")):
            raise ValueError("invalid completed resource evidence")
        if len(acceptance) != 1 or acceptance[0].get("test_id") != "transport.synthetic.harmless" or acceptance[0].get("status") != "passed" or not isinstance(acceptance[0].get("duration_ms"), int) or not 0 <= acceptance[0]["duration_ms"] <= 45000:
            raise ValueError("invalid completed acceptance evidence")
    return response


def ssh_exchange(host, key, known_hosts, wire):
    command = [
        "ssh", "-T", "-i", key, "-o", f"UserKnownHostsFile={known_hosts}",
        "-o", "StrictHostKeyChecking=yes", "-o", "BatchMode=yes",
        "-o", "IdentitiesOnly=yes", "-o", "PasswordAuthentication=no",
        "-o", "KbdInteractiveAuthentication=no", "-o", "PreferredAuthentications=publickey",
        "-o", "ClearAllForwardings=yes", f"qaos-broker@{host}",
    ]
    return subprocess.run(
        command, input=wire, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        timeout=75, check=False,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", required=True)
    parser.add_argument("--key", required=True)
    parser.add_argument("--known-hosts", required=True)
    args = parser.parse_args()
    request, wire = build_probe()
    result = ssh_exchange(args.host, args.key, args.known_hosts, wire)
    if result.returncode != 0:
        return 1
    response = validate_response(result.stdout, request)
    print(response["outcome"])
    return 0 if response["outcome"] == "completed" else 1


if __name__ == "__main__":
    sys.exit(main())
