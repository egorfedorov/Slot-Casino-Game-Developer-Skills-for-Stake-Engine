#!/usr/bin/env python3
"""Validate slot UX specification contract."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ALLOWED_CONTROL_TYPES = {
    "spin",
    "bet",
    "autoplay",
    "turbo",
    "menu",
    "sound",
    "help",
    "balance",
    "history",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Path to slot_ux_spec.json")
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
    for key in ("name", "views", "controls", "states", "interactions", "accessibility"):
        if key not in data:
            errors.append(f"missing top-level key '{key}'")

    views = data.get("views", {})
    controls = data.get("controls", [])
    states = data.get("states", [])
    interactions = data.get("interactions", [])
    accessibility = data.get("accessibility", {})

    if not isinstance(views, dict):
        errors.append("views must be object")
        views = {}
    for v in ("desktop", "mobile"):
        if v not in views:
            errors.append(f"views missing '{v}'")

    if not isinstance(controls, list) or not controls:
        errors.append("controls must be non-empty array")
        controls = []
    control_ids: set[str] = set()
    for i, ctrl in enumerate(controls):
        if not isinstance(ctrl, dict):
            errors.append(f"controls[{i}] must be object")
            continue
        for key in ("id", "type", "priority"):
            if key not in ctrl:
                errors.append(f"controls[{i}] missing '{key}'")
        if any(key not in ctrl for key in ("id", "type", "priority")):
            continue
        cid = str(ctrl["id"])
        ctype = str(ctrl["type"])
        if cid in control_ids:
            errors.append(f"duplicate control id '{cid}'")
        control_ids.add(cid)
        if ctype not in ALLOWED_CONTROL_TYPES:
            errors.append(f"controls[{i}] unsupported type '{ctype}'")
        try:
            priority = int(ctrl["priority"])
            if priority < 0:
                errors.append(f"controls[{i}] priority must be >= 0")
        except Exception:
            errors.append(f"controls[{i}] priority must be integer")

    if not isinstance(states, list) or not states:
        errors.append("states must be non-empty array")
        states = []
    state_names: set[str] = set()
    transition_pairs: set[tuple[str, str]] = set()
    for i, st in enumerate(states):
        if isinstance(st, str):
            name = st
            transitions = []
        elif isinstance(st, dict):
            name = str(st.get("name", ""))
            transitions = st.get("transitions", [])
        else:
            errors.append(f"states[{i}] invalid entry")
            continue
        if not name:
            errors.append(f"states[{i}] missing name")
            continue
        if name in state_names:
            errors.append(f"duplicate state '{name}'")
        state_names.add(name)
        if transitions is None:
            transitions = []
        if not isinstance(transitions, list):
            errors.append(f"states[{i}].transitions must be array")
            continue
        for t in transitions:
            transition_pairs.add((name, str(t)))

    if not isinstance(interactions, list):
        errors.append("interactions must be array")
        interactions = []
    for i, inter in enumerate(interactions):
        if not isinstance(inter, dict):
            errors.append(f"interactions[{i}] must be object")
            continue
        for key in ("trigger", "sourceControl", "targetState", "feedbackMs"):
            if key not in inter:
                errors.append(f"interactions[{i}] missing '{key}'")
        if any(key not in inter for key in ("trigger", "sourceControl", "targetState", "feedbackMs")):
            continue
        source = str(inter["sourceControl"])
        target_state = str(inter["targetState"])
        if source not in control_ids:
            errors.append(f"interactions[{i}] unknown sourceControl '{source}'")
        if target_state not in state_names:
            errors.append(f"interactions[{i}] unknown targetState '{target_state}'")
        try:
            feedback = int(inter["feedbackMs"])
            if feedback < 0:
                errors.append(f"interactions[{i}] feedbackMs must be >= 0")
            if feedback > 10000:
                errors.append(f"interactions[{i}] feedbackMs too large (>10000)")
        except Exception:
            errors.append(f"interactions[{i}] feedbackMs must be integer")

    if not isinstance(accessibility, dict):
        errors.append("accessibility must be object")
        accessibility = {}
    try:
        min_touch = int(accessibility.get("minTouchTargetPx", 0))
        if min_touch < 44:
            errors.append("accessibility.minTouchTargetPx must be >= 44")
    except Exception:
        errors.append("accessibility.minTouchTargetPx must be integer")
    if accessibility.get("reducedMotionSupport") is not True:
        errors.append("accessibility.reducedMotionSupport must be true")
    if accessibility.get("contrastModeSupport") is not True:
        errors.append("accessibility.contrastModeSupport must be true")

    summary = {
        "name": data.get("name"),
        "passed": len(errors) == 0,
        "counts": {
            "controls": len(control_ids),
            "states": len(state_names),
            "interactions": len(interactions),
            "transitions": len(transition_pairs),
        },
        "errors": errors,
    }
    print(json.dumps(summary, separators=(",", ":")))
    return 0 if summary["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
