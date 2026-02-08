#!/usr/bin/env python3
"""Compare latency percentile snapshots and detect regressions."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


PERCENTILE_KEYS = ("p50", "p95", "p99", "p999")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", required=True, help="Baseline latency JSON")
    parser.add_argument("--current", required=True, help="Current latency JSON")
    parser.add_argument(
        "--threshold-pct",
        type=float,
        default=5.0,
        help="Max allowed regression percentage per percentile",
    )
    return parser.parse_args()


def load_metrics(path: Path) -> dict[str, float]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: root must be object")

    metrics: dict[str, float] = {}
    for key in PERCENTILE_KEYS:
        if key not in data:
            continue
        value = float(data[key])
        if value <= 0:
            raise ValueError(f"{path}: {key} must be > 0")
        metrics[key] = value
    if not metrics:
        raise ValueError(f"{path}: no percentile keys found ({', '.join(PERCENTILE_KEYS)})")
    return metrics


def delta_pct(base: float, current: float) -> float:
    return ((current - base) / base) * 100.0


def main() -> int:
    args = parse_args()
    baseline_path = Path(args.baseline)
    current_path = Path(args.current)
    if not baseline_path.exists():
        print(json.dumps({"passed": False, "errors": [f"baseline not found: {baseline_path}"]}))
        return 2
    if not current_path.exists():
        print(json.dumps({"passed": False, "errors": [f"current not found: {current_path}"]}))
        return 2

    try:
        baseline = load_metrics(baseline_path)
        current = load_metrics(current_path)
    except Exception as exc:
        print(json.dumps({"passed": False, "errors": [str(exc)]}))
        return 2

    common = [k for k in PERCENTILE_KEYS if k in baseline and k in current]
    if not common:
        print(json.dumps({"passed": False, "errors": ["no common percentile keys"]}))
        return 2

    regressions: list[dict[str, Any]] = []
    improvements: list[dict[str, Any]] = []
    compared: dict[str, Any] = {}
    for key in common:
        base_val = baseline[key]
        cur_val = current[key]
        delta = delta_pct(base_val, cur_val)
        compared[key] = {
            "baseline_ms": base_val,
            "current_ms": cur_val,
            "delta_pct": delta,
        }
        if delta >= args.threshold_pct:
            regressions.append({"metric": key, "delta_pct": delta})
        elif delta <= -abs(args.threshold_pct):
            improvements.append({"metric": key, "delta_pct": delta})

    regressions.sort(key=lambda r: r["delta_pct"], reverse=True)
    improvements.sort(key=lambda r: r["delta_pct"])

    summary = {
        "threshold_pct": args.threshold_pct,
        "compared": compared,
        "regressions": regressions,
        "improvements": improvements,
        "passed": len(regressions) == 0,
    }
    print(json.dumps(summary, separators=(",", ":")))
    return 0 if summary["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
