#!/usr/bin/env python3
"""Evaluate RTP simulation runs against target and tolerance."""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Path to .jsonl or .csv run file")
    parser.add_argument("--target-rtp", required=True, type=float)
    parser.add_argument("--tolerance", required=True, type=float)
    parser.add_argument("--min-runs", type=int, default=5)
    parser.add_argument("--rtp-field", default="rtp")
    parser.add_argument("--total-win-field", default="total_win")
    parser.add_argument("--total-bet-field", default="total_bet")
    return parser.parse_args()


def read_runs(path: Path) -> list[dict[str, Any]]:
    if path.suffix.lower() == ".jsonl":
        rows = []
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rows.append(json.loads(line))
        return rows
    if path.suffix.lower() == ".csv":
        with path.open("r", encoding="utf-8", newline="") as handle:
            return list(csv.DictReader(handle))
    raise ValueError("input must be .jsonl or .csv")


def coerce_float(value: Any) -> float:
    if isinstance(value, (float, int)):
        return float(value)
    return float(str(value).strip())


def extract_rtp(row: dict[str, Any], args: argparse.Namespace) -> float:
    if args.rtp_field in row and str(row[args.rtp_field]).strip() != "":
        return coerce_float(row[args.rtp_field])
    has_win = args.total_win_field in row and str(row[args.total_win_field]).strip() != ""
    has_bet = args.total_bet_field in row and str(row[args.total_bet_field]).strip() != ""
    if has_win and has_bet:
        total_win = coerce_float(row[args.total_win_field])
        total_bet = coerce_float(row[args.total_bet_field])
        if total_bet <= 0:
            raise ValueError("total_bet must be > 0")
        return total_win / total_bet
    raise ValueError(
        f"row must contain {args.rtp_field} or both {args.total_win_field} and {args.total_bet_field}"
    )


def summarize(rtps: list[float]) -> dict[str, float]:
    n = len(rtps)
    mean = sum(rtps) / n
    if n < 2:
        return {"mean": mean, "stdev": 0.0, "sem": 0.0, "ci95": 0.0}
    variance = sum((x - mean) ** 2 for x in rtps) / (n - 1)
    stdev = math.sqrt(variance)
    sem = stdev / math.sqrt(n)
    ci95 = 1.96 * sem
    return {"mean": mean, "stdev": stdev, "sem": sem, "ci95": ci95}


def main() -> int:
    args = parse_args()
    path = Path(args.input)
    if not path.exists():
        print(f"input not found: {path}", file=sys.stderr)
        return 2

    try:
        rows = read_runs(path)
    except Exception as exc:
        print(f"failed to read input: {exc}", file=sys.stderr)
        return 2

    rtps: list[float] = []
    for idx, row in enumerate(rows, start=1):
        try:
            rtp = extract_rtp(row, args)
            rtps.append(rtp)
        except Exception as exc:
            print(f"line {idx}: invalid row: {exc}", file=sys.stderr)
            return 2

    if len(rtps) < args.min_runs:
        print(
            f"insufficient runs: got {len(rtps)}, require at least {args.min_runs}",
            file=sys.stderr,
        )
        return 2

    stats = summarize(rtps)
    mean = stats["mean"]
    ci95 = stats["ci95"]

    lower_target = args.target_rtp - args.tolerance
    upper_target = args.target_rtp + args.tolerance

    mean_in_band = lower_target <= mean <= upper_target
    ci_inside_band = (mean - ci95) >= lower_target and (mean + ci95) <= upper_target
    passed = mean_in_band and ci_inside_band

    summary = {
        "runs": len(rtps),
        "target_rtp": args.target_rtp,
        "tolerance": args.tolerance,
        "band": {"lower": lower_target, "upper": upper_target},
        "mean_rtp": mean,
        "stdev": stats["stdev"],
        "sem": stats["sem"],
        "ci95": ci95,
        "drift_vs_target": mean - args.target_rtp,
        "mean_in_band": mean_in_band,
        "ci_inside_band": ci_inside_band,
        "passed": passed,
    }
    print(json.dumps(summary, separators=(",", ":")))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
