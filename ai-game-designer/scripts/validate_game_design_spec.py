#!/usr/bin/env python3
"""Validate AI game design spec contract."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REQUIRED_LOOPS = ("core", "progression", "retention")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Path to game_design_spec.json")
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
    for key in ("name", "loops", "features", "systems", "constraints", "telemetry"):
        if key not in data:
            errors.append(f"missing top-level key '{key}'")

    loops = data.get("loops", {})
    features = data.get("features", [])
    systems = data.get("systems", {})
    constraints = data.get("constraints", {})
    telemetry = data.get("telemetry", {})

    if not isinstance(loops, dict):
        errors.append("loops must be object")
        loops = {}
    for loop_name in REQUIRED_LOOPS:
        if loop_name not in loops:
            errors.append(f"loops missing '{loop_name}'")

    if not isinstance(features, list) or not features:
        errors.append("features must be non-empty array")
        features = []
    feature_ids: set[str] = set()
    for i, feat in enumerate(features):
        if not isinstance(feat, dict):
            errors.append(f"features[{i}] must be object")
            continue
        for key in ("id", "loop", "dependsOn"):
            if key not in feat:
                errors.append(f"features[{i}] missing '{key}'")
        if any(key not in feat for key in ("id", "loop", "dependsOn")):
            continue
        fid = str(feat["id"])
        loop = str(feat["loop"])
        deps = feat["dependsOn"]
        if fid in feature_ids:
            errors.append(f"duplicate feature id '{fid}'")
        feature_ids.add(fid)
        if loop not in REQUIRED_LOOPS:
            errors.append(f"features[{i}] unknown loop '{loop}'")
        if not isinstance(deps, list):
            errors.append(f"features[{i}].dependsOn must be array")

    for i, feat in enumerate(features):
        if not isinstance(feat, dict) or "id" not in feat or "dependsOn" not in feat:
            continue
        deps = feat["dependsOn"]
        if not isinstance(deps, list):
            continue
        for dep in deps:
            dep_id = str(dep)
            if dep_id not in feature_ids:
                errors.append(f"features[{i}] references unknown dependency '{dep_id}'")

    if not isinstance(systems, dict):
        errors.append("systems must be object")
        systems = {}
    economy = systems.get("economy", {})
    progression = systems.get("progression", {})
    if not isinstance(economy, dict):
        errors.append("systems.economy must be object")
        economy = {}
    if not isinstance(progression, dict):
        errors.append("systems.progression must be object")
        progression = {}

    sources = economy.get("sources", [])
    sinks = economy.get("sinks", [])
    if not isinstance(sources, list) or len(sources) == 0:
        errors.append("systems.economy.sources must be non-empty array")
    if not isinstance(sinks, list) or len(sinks) == 0:
        errors.append("systems.economy.sinks must be non-empty array")

    gates = progression.get("gates", [])
    if not isinstance(gates, list):
        errors.append("systems.progression.gates must be array")
        gates = []
    for i, gate in enumerate(gates):
        if not isinstance(gate, dict):
            errors.append(f"systems.progression.gates[{i}] must be object")
            continue
        if "id" not in gate or "unlockCondition" not in gate:
            errors.append(f"systems.progression.gates[{i}] missing id or unlockCondition")

    if not isinstance(constraints, dict):
        errors.append("constraints must be object")
        constraints = {}
    for k in ("maxSessionMinutes", "maxDailyReward", "antiExploitRules"):
        if k not in constraints:
            errors.append(f"constraints missing '{k}'")
    if "antiExploitRules" in constraints and not isinstance(
        constraints.get("antiExploitRules"), list
    ):
        errors.append("constraints.antiExploitRules must be array")

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
            "features": len(feature_ids),
            "sources": len(sources) if isinstance(sources, list) else 0,
            "sinks": len(sinks) if isinstance(sinks, list) else 0,
            "gates": len(gates) if isinstance(gates, list) else 0,
        },
        "errors": errors,
    }
    print(json.dumps(summary, separators=(",", ":")))
    return 0 if summary["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
