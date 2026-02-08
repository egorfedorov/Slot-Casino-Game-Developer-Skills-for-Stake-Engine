#!/usr/bin/env python3
"""Validate auto-balancing run outputs against targets and constraints."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Path to balance_runs.json")
    parser.add_argument("--spec", required=True, help="Path to target_spec.json")
    return parser.parse_args()


def compare(operator: str, observed: float, expected: float) -> bool:
    if operator == "<=":
        return observed <= expected
    if operator == "<":
        return observed < expected
    if operator == ">=":
        return observed >= expected
    if operator == ">":
        return observed > expected
    if operator == "==":
        return observed == expected
    raise ValueError(f"unsupported operator '{operator}'")


def main() -> int:
    args = parse_args()
    input_path = Path(args.input)
    spec_path = Path(args.spec)
    if not input_path.exists():
        print(json.dumps({"passed": False, "errors": [f"input not found: {input_path}"]}))
        return 2
    if not spec_path.exists():
        print(json.dumps({"passed": False, "errors": [f"spec not found: {spec_path}"]}))
        return 2

    try:
        runs_doc = json.loads(input_path.read_text(encoding="utf-8"))
        spec_doc = json.loads(spec_path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(json.dumps({"passed": False, "errors": [f"invalid JSON: {exc}"]}))
        return 2

    errors: list[str] = []

    runs = runs_doc.get("runs", []) if isinstance(runs_doc, dict) else []
    if not isinstance(runs, list) or len(runs) == 0:
        errors.append("input.runs must be non-empty array")
        runs = []

    min_runs = spec_doc.get("minRuns", 1) if isinstance(spec_doc, dict) else 1
    try:
        min_runs_int = int(min_runs)
        if min_runs_int <= 0:
            errors.append("spec.minRuns must be > 0")
            min_runs_int = 1
    except Exception:
        errors.append("spec.minRuns must be integer")
        min_runs_int = 1

    targets = spec_doc.get("targets", []) if isinstance(spec_doc, dict) else []
    constraints = spec_doc.get("hardConstraints", []) if isinstance(spec_doc, dict) else []

    if not isinstance(targets, list) or len(targets) == 0:
        errors.append("spec.targets must be non-empty array")
        targets = []
    if not isinstance(constraints, list):
        errors.append("spec.hardConstraints must be array")
        constraints = []

    latest_metrics: dict[str, float] = {}
    baseline_metrics: dict[str, float] = {}
    best_metrics: dict[str, float] = {}

    if runs:
        first = runs[0] if isinstance(runs[0], dict) else {}
        last = runs[-1] if isinstance(runs[-1], dict) else {}
        baseline_metrics = first.get("metrics", {}) if isinstance(first, dict) else {}
        latest_metrics = last.get("metrics", {}) if isinstance(last, dict) else {}

    metric_rows: list[dict[str, Any]] = []
    metric_failures = 0
    for i, t in enumerate(targets):
        if not isinstance(t, dict):
            errors.append(f"targets[{i}] must be object")
            continue
        for key in ("name", "target", "tolerance"):
            if key not in t:
                errors.append(f"targets[{i}] missing '{key}'")
        if any(key not in t for key in ("name", "target", "tolerance")):
            continue

        name = str(t["name"])
        try:
            target = float(t["target"])
            tolerance = float(t["tolerance"])
        except Exception:
            errors.append(f"targets[{i}] target/tolerance must be numeric")
            continue

        if name not in latest_metrics:
            errors.append(f"latest run missing metric '{name}'")
            continue

        observed = float(latest_metrics[name])
        delta = observed - target
        passed = abs(delta) <= tolerance
        if not passed:
            metric_failures += 1

        if name not in best_metrics:
            best_metrics[name] = observed

        for run in runs:
            if not isinstance(run, dict):
                continue
            m = run.get("metrics", {})
            if not isinstance(m, dict) or name not in m:
                continue
            val = float(m[name])
            if abs(val - target) < abs(best_metrics[name] - target):
                best_metrics[name] = val

        metric_rows.append(
            {
                "name": name,
                "target": target,
                "tolerance": tolerance,
                "baseline": baseline_metrics.get(name),
                "best": best_metrics.get(name),
                "final": observed,
                "delta": delta,
                "passed": passed,
            }
        )

    constraint_rows: list[dict[str, Any]] = []
    constraint_failures = 0
    for i, c in enumerate(constraints):
        if not isinstance(c, dict):
            errors.append(f"hardConstraints[{i}] must be object")
            continue
        for key in ("name", "operator", "value"):
            if key not in c:
                errors.append(f"hardConstraints[{i}] missing '{key}'")
        if any(key not in c for key in ("name", "operator", "value")):
            continue

        name = str(c["name"])
        operator = str(c["operator"])
        try:
            threshold = float(c["value"])
        except Exception:
            errors.append(f"hardConstraints[{i}] value must be numeric")
            continue

        if name not in latest_metrics:
            errors.append(f"latest run missing constraint metric '{name}'")
            continue

        observed = float(latest_metrics[name])
        try:
            passed = compare(operator, observed, threshold)
        except Exception as exc:
            errors.append(f"hardConstraints[{i}] {exc}")
            continue

        if not passed:
            constraint_failures += 1

        constraint_rows.append(
            {
                "name": name,
                "operator": operator,
                "threshold": threshold,
                "final": observed,
                "passed": passed,
            }
        )

    if len(runs) < min_runs_int:
        errors.append(f"run count {len(runs)} is below minRuns {min_runs_int}")

    passed = (
        len(errors) == 0
        and metric_failures == 0
        and constraint_failures == 0
        and len(runs) >= min_runs_int
    )

    summary = {
        "passed": passed,
        "runs": len(runs),
        "minRuns": min_runs_int,
        "metricFailures": metric_failures,
        "constraintFailures": constraint_failures,
        "metrics": metric_rows,
        "constraints": constraint_rows,
        "errors": errors,
    }
    print(json.dumps(summary, separators=(",", ":")))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
