#!/usr/bin/env python3
"""Compare Google Benchmark JSON results and detect regressions."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", required=True, help="Baseline benchmark JSON")
    parser.add_argument("--current", required=True, help="Current benchmark JSON")
    parser.add_argument(
        "--metric",
        default="cpu_time",
        choices=["cpu_time", "real_time"],
        help="Metric to compare",
    )
    parser.add_argument(
        "--regression-threshold",
        type=float,
        default=5.0,
        help="Regression percentage threshold (positive)",
    )
    parser.add_argument(
        "--improvement-threshold",
        type=float,
        default=5.0,
        help="Improvement percentage threshold (positive)",
    )
    return parser.parse_args()


def load_benchmarks(path: Path, metric: str) -> dict[str, float]:
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = data.get("benchmarks")
    if not isinstance(rows, list):
        raise ValueError(f"{path}: missing 'benchmarks' array")

    result: dict[str, float] = {}
    for idx, row in enumerate(rows):
        if not isinstance(row, dict):
            continue
        name = row.get("name")
        if not isinstance(name, str):
            continue
        value = row.get(metric)
        if value is None:
            continue
        try:
            parsed = float(value)
        except Exception as exc:
            raise ValueError(f"{path}: invalid {metric} at row {idx}: {exc}") from exc
        if parsed <= 0:
            continue
        result[name] = parsed
    return result


def percent_delta(baseline: float, current: float) -> float:
    return ((current - baseline) / baseline) * 100.0


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
        base = load_benchmarks(baseline_path, args.metric)
        curr = load_benchmarks(current_path, args.metric)
    except Exception as exc:
        print(json.dumps({"passed": False, "errors": [str(exc)]}))
        return 2

    common = sorted(set(base) & set(curr))
    if not common:
        print(json.dumps({"passed": False, "errors": ["no common benchmark names"]}))
        return 2

    regressions: list[dict[str, Any]] = []
    improvements: list[dict[str, Any]] = []
    compared: list[dict[str, Any]] = []
    for name in common:
        b = base[name]
        c = curr[name]
        delta = percent_delta(b, c)
        row = {"name": name, "baseline": b, "current": c, "delta_pct": delta}
        compared.append(row)
        if delta >= args.regression_threshold:
            regressions.append(row)
        elif delta <= -abs(args.improvement_threshold):
            improvements.append(row)

    regressions.sort(key=lambda r: r["delta_pct"], reverse=True)
    improvements.sort(key=lambda r: r["delta_pct"])

    summary = {
        "metric": args.metric,
        "regression_threshold_pct": args.regression_threshold,
        "improvement_threshold_pct": args.improvement_threshold,
        "benchmarks_compared": len(compared),
        "missing_in_current": sorted(set(base) - set(curr)),
        "missing_in_baseline": sorted(set(curr) - set(base)),
        "regressions_count": len(regressions),
        "improvements_count": len(improvements),
        "top_regressions": regressions[:10],
        "top_improvements": improvements[:10],
        "passed": len(regressions) == 0,
    }
    print(json.dumps(summary, separators=(",", ":")))
    return 0 if summary["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
