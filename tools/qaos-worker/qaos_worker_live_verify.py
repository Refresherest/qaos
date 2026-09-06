#!/usr/bin/env python3
"""Bounded live negative verification for the restricted worker transport."""

from __future__ import annotations

import argparse
import copy

from qaos_worker_exchange import MEMBER_LIMIT, REQUEST_LIMIT, canonical_json, encode_frame
from qaos_worker_probe import build_probe, ssh_exchange, validate_response


PAYLOADS = (
    b"QAOS synthetic acceptance bytes\n",
    b"QAOS synthetic candidate bytes\n",
)


def request_wire(request: dict) -> bytes:
    wire = encode_frame(canonical_json(request), REQUEST_LIMIT)
    for payload in PAYLOADS:
        wire += encode_frame(payload, MEMBER_LIMIT)
    return wire


def expect_pre_correlation_rejection(host, key, known_hosts, request):
    result = ssh_exchange(host, key, known_hosts, request_wire(request))
    if result.returncode != 1 or result.stdout:
        raise RuntimeError("expected silent pre-correlation rejection")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", required=True)
    parser.add_argument("--key", required=True)
    parser.add_argument("--known-hosts", required=True)
    args = parser.parse_args()

    request, wire = build_probe()
    first = ssh_exchange(args.host, args.key, args.known_hosts, wire)
    if first.returncode != 0:
        raise RuntimeError("initial exchange failed")
    if validate_response(first.stdout, request)["outcome"] != "completed":
        raise RuntimeError("initial exchange did not complete")

    replay = ssh_exchange(args.host, args.key, args.known_hosts, wire)
    if replay.returncode != 0:
        raise RuntimeError("replay response transport failed")
    if validate_response(replay.stdout, request)["outcome"] != "policy_rejected":
        raise RuntimeError("replay was not rejected")

    unexpected = copy.deepcopy(request)
    unexpected["unexpected"] = True
    expect_pre_correlation_rejection(args.host, args.key, args.known_hosts, unexpected)

    unsafe_path = copy.deepcopy(request)
    unsafe_path["request_id"] = "00000000-0000-4000-8000-000000000001"
    unsafe_path["members"][0]["path"] = "../acceptance.txt"
    expect_pre_correlation_rejection(args.host, args.key, args.known_hosts, unsafe_path)

    bad_hash = copy.deepcopy(request)
    bad_hash["request_id"] = "00000000-0000-4000-8000-000000000002"
    bad_hash["members"][0]["sha256"] = "0" * 64
    expect_pre_correlation_rejection(args.host, args.key, args.known_hosts, bad_hash)

    print("live-negative-suite-passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
