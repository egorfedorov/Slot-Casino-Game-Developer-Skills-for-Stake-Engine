#!/usr/bin/env python3
"""Validate event animation timeline contract JSON."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ALLOWED_EASINGS = {
    "linear",
    "easeIn",
    "easeOut",
    "easeInOut",
    "backOut",
    "bounceOut",
    "elasticOut",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Path to animation_timeline.json")
    return parser.parse_args()


def as_name_set(items: list[Any], key: str, label: str, errors: list[str]) -> set[str]:
    out: set[str] = set()
    for i, item in enumerate(items):
        if isinstance(item, str):
            name = item
        elif isinstance(item, dict) and key in item:
            name = str(item[key])
        else:
            errors.append(f"{label}[{i}] invalid entry")
            continue
        if name in out:
            errors.append(f"{label} duplicate '{name}'")
        out.add(name)
    return out


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
    for key in ("name", "states", "events", "transitions", "timelines"):
        if key not in data:
            errors.append(f"missing top-level key '{key}'")

    states_raw = data.get("states", [])
    events_raw = data.get("events", [])
    transitions_raw = data.get("transitions", [])
    timelines_raw = data.get("timelines", [])

    if not isinstance(states_raw, list):
        errors.append("states must be array")
        states_raw = []
    if not isinstance(events_raw, list):
        errors.append("events must be array")
        events_raw = []
    if not isinstance(transitions_raw, list):
        errors.append("transitions must be array")
        transitions_raw = []
    if not isinstance(timelines_raw, list):
        errors.append("timelines must be array")
        timelines_raw = []

    states = as_name_set(states_raw, "name", "states", errors)
    events = as_name_set(events_raw, "name", "events", errors)

    transition_keys: set[tuple[str, str, str]] = set()
    for i, tr in enumerate(transitions_raw):
        if not isinstance(tr, dict):
            errors.append(f"transitions[{i}] must be object")
            continue
        for key in ("from", "event", "to"):
            if key not in tr:
                errors.append(f"transitions[{i}] missing '{key}'")
        if any(key not in tr for key in ("from", "event", "to")):
            continue
        src = str(tr["from"])
        evt = str(tr["event"])
        dst = str(tr["to"])
        if src not in states:
            errors.append(f"transitions[{i}] unknown from state '{src}'")
        if dst not in states:
            errors.append(f"transitions[{i}] unknown to state '{dst}'")
        if evt not in events:
            errors.append(f"transitions[{i}] unknown event '{evt}'")
        key = (src, evt, dst)
        if key in transition_keys:
            errors.append(f"duplicate transition {key}")
        transition_keys.add(key)

    seen_timeline_keys: set[tuple[str, str, str]] = set()
    for i, tl in enumerate(timelines_raw):
        if not isinstance(tl, dict):
            errors.append(f"timelines[{i}] must be object")
            continue
        for key in ("event", "fromState", "toState", "steps"):
            if key not in tl:
                errors.append(f"timelines[{i}] missing '{key}'")
        if any(key not in tl for key in ("event", "fromState", "toState", "steps")):
            continue

        evt = str(tl["event"])
        src = str(tl["fromState"])
        dst = str(tl["toState"])
        steps = tl["steps"]

        if evt not in events:
            errors.append(f"timelines[{i}] unknown event '{evt}'")
        if src not in states:
            errors.append(f"timelines[{i}] unknown fromState '{src}'")
        if dst not in states:
            errors.append(f"timelines[{i}] unknown toState '{dst}'")

        key = (src, evt, dst)
        if key in seen_timeline_keys:
            errors.append(f"duplicate timeline mapping {key}")
        seen_timeline_keys.add(key)

        if key not in transition_keys:
            errors.append(f"timelines[{i}] has no matching transition {key}")

        if not isinstance(steps, list) or not steps:
            errors.append(f"timelines[{i}] steps must be non-empty array")
            continue

        last_start = -1.0
        step_ids: set[str] = set()
        for s_idx, step in enumerate(steps):
            if not isinstance(step, dict):
                errors.append(f"timelines[{i}].steps[{s_idx}] must be object")
                continue
            for key_name in ("id", "target", "startMs", "durationMs", "easing"):
                if key_name not in step:
                    errors.append(f"timelines[{i}].steps[{s_idx}] missing '{key_name}'")
            if any(k not in step for k in ("id", "target", "startMs", "durationMs", "easing")):
                continue

            step_id = str(step["id"])
            if step_id in step_ids:
                errors.append(f"timelines[{i}] duplicate step id '{step_id}'")
            step_ids.add(step_id)

            try:
                start_ms = float(step["startMs"])
                duration_ms = float(step["durationMs"])
            except Exception:
                errors.append(f"timelines[{i}].steps[{s_idx}] startMs/durationMs must be numeric")
                continue

            easing = str(step["easing"])
            if start_ms < 0:
                errors.append(f"timelines[{i}].steps[{s_idx}] startMs must be >= 0")
            if duration_ms <= 0:
                errors.append(f"timelines[{i}].steps[{s_idx}] durationMs must be > 0")
            if easing not in ALLOWED_EASINGS:
                errors.append(
                    f"timelines[{i}].steps[{s_idx}] unsupported easing '{easing}'"
                )
            if start_ms < last_start:
                errors.append(f"timelines[{i}] steps out of order at index {s_idx}")
            last_start = start_ms

    summary = {
        "name": data.get("name"),
        "passed": len(errors) == 0,
        "counts": {
            "states": len(states),
            "events": len(events),
            "transitions": len(transition_keys),
            "timelines": len(seen_timeline_keys),
        },
        "errors": errors,
    }
    print(json.dumps(summary, separators=(",", ":")))
    return 0 if summary["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
