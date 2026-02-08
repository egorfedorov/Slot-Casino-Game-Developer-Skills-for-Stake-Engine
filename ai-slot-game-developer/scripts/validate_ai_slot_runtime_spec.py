#!/usr/bin/env python3
"""Validate AI slot runtime specification."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Path to ai_slot_runtime_spec.json")
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
    for key in ("name", "modes", "aiSystems", "models", "runtime", "safety", "telemetry"):
        if key not in data:
            errors.append(f"missing top-level key '{key}'")

    modes = data.get("modes", [])
    systems = data.get("aiSystems", [])
    models = data.get("models", [])
    runtime = data.get("runtime", {})
    safety = data.get("safety", {})
    telemetry = data.get("telemetry", {})

    if not isinstance(modes, list) or not modes:
        errors.append("modes must be non-empty array")
        modes = []
    mode_ids: set[str] = set()
    for i, mode in enumerate(modes):
        if isinstance(mode, str):
            mid = mode
        elif isinstance(mode, dict) and "id" in mode:
            mid = str(mode["id"])
        else:
            errors.append(f"modes[{i}] invalid entry")
            continue
        if mid in mode_ids:
            errors.append(f"duplicate mode id '{mid}'")
        mode_ids.add(mid)

    if not isinstance(systems, list) or not systems:
        errors.append("aiSystems must be non-empty array")
        systems = []
    system_ids: set[str] = set()
    used_mode_refs: set[str] = set()
    for i, s in enumerate(systems):
        if not isinstance(s, dict):
            errors.append(f"aiSystems[{i}] must be object")
            continue
        for key in ("id", "modelId", "modes", "maxLatencyMs"):
            if key not in s:
                errors.append(f"aiSystems[{i}] missing '{key}'")
        if any(key not in s for key in ("id", "modelId", "modes", "maxLatencyMs")):
            continue

        sid = str(s["id"])
        if sid in system_ids:
            errors.append(f"duplicate aiSystem id '{sid}'")
        system_ids.add(sid)

        modes_ref = s["modes"]
        if not isinstance(modes_ref, list) or len(modes_ref) == 0:
            errors.append(f"aiSystems[{i}].modes must be non-empty array")
        else:
            for mref in modes_ref:
                mref_s = str(mref)
                used_mode_refs.add(mref_s)
                if mref_s not in mode_ids:
                    errors.append(f"aiSystems[{i}] references unknown mode '{mref_s}'")

        try:
            lat = float(s["maxLatencyMs"])
            if lat <= 0:
                errors.append(f"aiSystems[{i}].maxLatencyMs must be > 0")
        except Exception:
            errors.append(f"aiSystems[{i}].maxLatencyMs must be numeric")

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

    for i, ref in fallback_refs:
        if ref not in model_ids:
            errors.append(f"models[{i}] references unknown fallbackModelId '{ref}'")

    for i, s in enumerate(systems):
        if not isinstance(s, dict) or "modelId" not in s:
            continue
        model_id = str(s["modelId"])
        if model_id not in model_ids:
            errors.append(f"aiSystems[{i}] references unknown modelId '{model_id}'")

    if mode_ids and used_mode_refs and mode_ids - used_mode_refs:
        errors.append(f"unused modes in aiSystems mapping: {sorted(mode_ids - used_mode_refs)}")

    if not isinstance(runtime, dict):
        errors.append("runtime must be object")
        runtime = {}
    for key in ("tickIntegration", "fallbackPolicy", "maxQueueDepth"):
        if key not in runtime:
            errors.append(f"runtime missing '{key}'")
    if "maxQueueDepth" in runtime:
        try:
            q = int(runtime["maxQueueDepth"])
            if q <= 0:
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
            "modes": len(mode_ids),
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
