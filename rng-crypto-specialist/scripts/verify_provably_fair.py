#!/usr/bin/env python3
"""Verify provably fair transcripts using HMAC-SHA256 and rejection sampling."""

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import sys
from pathlib import Path
from typing import Any


def hmac_block(server_seed: str, client_seed: str, nonce: int, counter: int) -> bytes:
    message = f"{client_seed}:{nonce}:{counter}".encode("utf-8")
    return hmac.new(server_seed.encode("utf-8"), message, hashlib.sha256).digest()


def derive_unbiased_outcome(server_seed: str, client_seed: str, nonce: int, range_max: int) -> tuple[int, int]:
    if range_max <= 0:
        raise ValueError("range_max must be > 0")

    limit = (1 << 64) // range_max * range_max
    for counter in range(1_000_000):
        block = hmac_block(server_seed, client_seed, nonce, counter)
        value = int.from_bytes(block[:8], byteorder="big", signed=False)
        if value < limit:
            return value % range_max, counter
    raise RuntimeError("failed to derive unbiased value within retry limit")


def verify_row(row: dict[str, Any], default_range_max: int) -> tuple[bool, str]:
    for key in ("serverSeed", "clientSeed", "nonce"):
        if key not in row:
            return False, f"missing field: {key}"

    server_seed = str(row["serverSeed"])
    client_seed = str(row["clientSeed"])
    nonce = int(row["nonce"])
    range_max = int(row.get("rangeMax", default_range_max))
    outcome, counter = derive_unbiased_outcome(server_seed, client_seed, nonce, range_max)

    if "serverSeedHash" in row:
        actual_hash = hashlib.sha256(server_seed.encode("utf-8")).hexdigest()
        expected_hash = str(row["serverSeedHash"]).lower()
        if actual_hash != expected_hash:
            return False, f"serverSeedHash mismatch: expected={expected_hash} actual={actual_hash}"

    if "expectedOutcome" in row and int(row["expectedOutcome"]) != outcome:
        return False, f"outcome mismatch: expected={row['expectedOutcome']} actual={outcome}"

    return True, f"ok outcome={outcome} counter={counter}"


def run_single(args: argparse.Namespace) -> int:
    outcome, counter = derive_unbiased_outcome(
        args.server_seed, args.client_seed, args.nonce, args.range_max
    )
    payload = {
        "serverSeedHash": hashlib.sha256(args.server_seed.encode("utf-8")).hexdigest(),
        "clientSeed": args.client_seed,
        "nonce": args.nonce,
        "rangeMax": args.range_max,
        "derivedOutcome": outcome,
        "counterUsed": counter,
    }
    print(json.dumps(payload, separators=(",", ":")))
    return 0


def run_batch(args: argparse.Namespace) -> int:
    path = Path(args.input)
    if not path.exists():
        print(f"input not found: {path}", file=sys.stderr)
        return 2

    total = 0
    failed = 0
    for idx, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        total += 1
        try:
            row = json.loads(line)
            ok, detail = verify_row(row, args.default_range_max)
        except Exception as exc:
            ok, detail = False, f"parse/verify error: {exc}"
        if not ok:
            failed += 1
        print(f"line={idx} status={'PASS' if ok else 'FAIL'} {detail}")

    summary = {"total": total, "failed": failed, "passed": total - failed}
    print(json.dumps(summary, separators=(",", ":")))
    return 1 if failed else 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--server-seed")
    parser.add_argument("--client-seed")
    parser.add_argument("--nonce", type=int)
    parser.add_argument("--range-max", type=int, default=10_000)
    parser.add_argument("--input", help="Path to JSONL transcript")
    parser.add_argument("--default-range-max", type=int, default=10_000)
    args = parser.parse_args()

    single_mode = all(
        value is not None for value in (args.server_seed, args.client_seed, args.nonce)
    )
    if args.input and single_mode:
        parser.error("use either single mode args or --input batch mode, not both")
    if not args.input and not single_mode:
        parser.error("provide single mode args or --input")
    return args


def main() -> int:
    args = parse_args()
    if args.input:
        return run_batch(args)
    return run_single(args)


if __name__ == "__main__":
    raise SystemExit(main())
