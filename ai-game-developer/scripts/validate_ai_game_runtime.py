#!/usr/bin/env python3
"""Validate AI game runtime specification."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Path to ai_game_runtime_spec.json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    path = Path(args.input)
    if not path.exists():
        print(json.dumps({"passed": False, "errors": [f"input not found: {path}"]}))
        return 2

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(json.dumps({"passed": False, "errors": [f"invalid JSON: {exc}"]}))
        return 2

    if not isinstance(data, dict):
        print(json.dumps({"passed": False, "errors": ["root must be object"]}))
        return 2

    errors: list[str] = []
    for key in ("name", "systems", "models", "runtime", "safety", "telemetry"):
        if key not in data:
            errors.append(f"missing top-level key '{key}'")

    systems = data.get("systems", [])
    models = data.get("models", [])
    runtime = data.get("runtime", {})
    safety = data.get("safety", {})
    telemetry = data.get("telemetry", {})

    if not isinstance(systems, list) or not systems:
        errors.append("systems must be non-empty array")
        systems = []
    system_ids: set[str] = set()
    for i, s in enumerate(systems):
        if not isinstance(s, dict):
            errors.append(f"systems[{i}] must be object")
            continue
        for key in ("id", "type", "updateHz", "maxLatencyMs"):
            if key not in s:
                errors.append(f"systems[{i}] missing '{key}'")
        if any(key not in s for key in ("id", "type", "updateHz", "maxLatencyMs")):
            continue
        sid = str(s["id"])
        if sid in system_ids:
            errors.append(f"duplicate system id '{sid}'")
        system_ids.add(sid)
        try:
            hz = float(s["updateHz"])
            lat = float(s["maxLatencyMs"])
            if hz <= 0:
                errors.append(f"systems[{i}] updateHz must be > 0")
            if lat <= 0:
                errors.append(f"systems[{i}] maxLatencyMs must be > 0")
        except Exception:
            errors.append(f"systems[{i}] updateHz/maxLatencyMs must be numeric")

    if not isinstance(models, list) or not models:
        errors.append("models must be non-empty array")
        models = []
    model_ids: set[str] = set()
    fallback_refs: list[tuple[int, str]] = []
    for i, m in enumerate(models):
        if not isinstance(m, dict):
            errors.append(f"models[{i}] must be object")
            continue
        for key in ("id", "provider", "purpose"):
            if key not in m:
                errors.append(f"models[{i}] missing '{key}'")
        if any(key not in m for key in ("id", "provider", "purpose")):
            continue
        mid = str(m["id"])
        if mid in model_ids:
            errors.append(f"duplicate model id '{mid}'")
        model_ids.add(mid)
        if "fallbackModelId" in m and m["fallbackModelId"] is not None:
            fallback_refs.append((i, str(m["fallbackModelId"])))

    for idx, ref in fallback_refs:
        if ref not in model_ids:
            errors.append(f"models[{idx}] references unknown fallbackModelId '{ref}'")

    if not isinstance(runtime, dict):
        errors.append("runtime must be object")
        runtime = {}
    for key in ("tickIntegration", "fallbackPolicy", "maxQueueDepth"):
        if key not in runtime:
            errors.append(f"runtime missing '{key}'")
    if "maxQueueDepth" in runtime:
        try:
            qd = int(runtime["maxQueueDepth"])
            if qd <= 0:
                errors.append("runtime.maxQueueDepth must be > 0")
        except Exception:
            errors.append("runtime.maxQueueDepth must be integer")

    if not isinstance(safety, dict):
        errors.append("safety must be object")
        safety = {}
    if safety.get("deterministicFallback") is not True:
        errors.append("safety.deterministicFallback must be true")
    failure_modes = safety.get("failureModes", [])
    if not isinstance(failure_modes, list) or len(failure_modes) == 0:
        errors.append("safety.failureModes must be non-empty array")

    if not isinstance(telemetry, dict):
        errors.append("telemetry must be object")
        telemetry = {}
    events = telemetry.get("events", [])
    metrics = telemetry.get("metrics", [])
    if not isinstance(events, list) or len(events) == 0:
        errors.append("telemetry.events must be non-empty array")
    if not isinstance(metrics, list) or len(metrics) == 0:
        errors.append("telemetry.metrics must be non-empty array")

    summary = {
        "name": data.get("name"),
        "passed": len(errors) == 0,
        "counts": {
            "systems": len(system_ids),
            "models": len(model_ids),
            "telemetryEvents": len(events) if isinstance(events, list) else 0,
            "telemetryMetrics": len(metrics) if isinstance(metrics, list) else 0,
        },
        "errors": errors,
    }
    print(json.dumps(summary, separators=(",", ":")))
    return 0 if summary["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
