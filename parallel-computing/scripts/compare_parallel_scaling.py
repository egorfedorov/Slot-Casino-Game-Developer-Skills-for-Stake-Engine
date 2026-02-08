#!/usr/bin/env python3
"""Compare baseline vs current parallel scaling runs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", required=True, help="Baseline scaling JSON")
    parser.add_argument("--current", required=True, help="Current scaling JSON")
    parser.add_argument(
        "--regression-threshold-pct",
        type=float,
        default=5.0,
        help="Throughput regression threshold percent",
    )
    parser.add_argument(
        "--efficiency-drop-threshold-pct",
        type=float,
        default=10.0,
        help="Efficiency drop threshold percent vs baseline at same threads",
    )
    return parser.parse_args()


def load_runs(path: Path) -> dict[int, float]:
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = data.get("runs")
    if not isinstance(rows, list):
        raise ValueError(f"{path}: missing 'runs' array")

    out: dict[int, float] = {}
    for i, row in enumerate(rows):
        if not isinstance(row, dict):
            raise ValueError(f"{path}: runs[{i}] must be object")
        if "threads" not in row or "throughput" not in row:
            raise ValueError(f"{path}: runs[{i}] must include threads and throughput")
        t = int(row["threads"])
        thr = float(row["throughput"])
        if t <= 0 or thr <= 0:
            raise ValueError(f"{path}: runs[{i}] invalid threads/throughput")
        out[t] = thr
    if 1 not in out:
        raise ValueError(f"{path}: runs must include threads=1 baseline")
    return out


def pct_delta(old: float, new: float) -> float:
    return ((new - old) / old) * 100.0


def efficiency(single_thread_throughput: float, throughput: float, threads: int) -> float:
    return throughput / (single_thread_throughput * threads)


def main() -> int:
    args = parse_args()
    b_path = Path(args.baseline)
    c_path = Path(args.current)
    if not b_path.exists():
        print(json.dumps({"passed": False, "errors": [f"baseline not found: {b_path}"]}))
        return 2
    if not c_path.exists():
        print(json.dumps({"passed": False, "errors": [f"current not found: {c_path}"]}))
        return 2

    try:
        base = load_runs(b_path)
        curr = load_runs(c_path)
    except Exception as exc:
        print(json.dumps({"passed": False, "errors": [str(exc)]}))
        return 2

    common_threads = sorted(set(base) & set(curr))
    if not common_threads:
        print(json.dumps({"passed": False, "errors": ["no common thread counts"]}))
        return 2

    base1 = base[1]
    curr1 = curr[1]
    rows: list[dict[str, Any]] = []
    regressions: list[dict[str, Any]] = []
    for t in common_threads:
        base_thr = base[t]
        curr_thr = curr[t]
        thr_delta = pct_delta(base_thr, curr_thr)
        base_eff = efficiency(base1, base_thr, t)
        curr_eff = efficiency(curr1, curr_thr, t)
        eff_delta = pct_delta(base_eff, curr_eff)
        row = {
            "threads": t,
            "baseline_throughput": base_thr,
            "current_throughput": curr_thr,
            "throughput_delta_pct": thr_delta,
            "baseline_efficiency": base_eff,
            "current_efficiency": curr_eff,
            "efficiency_delta_pct": eff_delta,
        }
        rows.append(row)

        if thr_delta <= -abs(args.regression_threshold_pct):
            regressions.append(
                {"threads": t, "type": "throughput", "delta_pct": thr_delta}
            )
        if eff_delta <= -abs(args.efficiency_drop_threshold_pct):
            regressions.append(
                {"threads": t, "type": "efficiency", "delta_pct": eff_delta}
            )

    regressions.sort(key=lambda r: r["delta_pct"])
    summary = {
        "threads_compared": common_threads,
        "regression_threshold_pct": args.regression_threshold_pct,
        "efficiency_drop_threshold_pct": args.efficiency_drop_threshold_pct,
        "rows": rows,
        "regressions": regressions,
        "missing_in_current": sorted(set(base) - set(curr)),
        "missing_in_baseline": sorted(set(curr) - set(base)),
        "passed": len(regressions) == 0,
    }
    print(json.dumps(summary, separators=(",", ":")))
    return 0 if summary["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
