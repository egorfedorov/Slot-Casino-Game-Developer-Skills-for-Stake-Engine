#!/usr/bin/env python3
"""Validate Pixi+Svelte integration contract JSON."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REQUIRED_TOP_LEVEL = (
    "name",
    "hostComponent",
    "pixiAdapter",
    "lifecycle",
    "events",
    "resize",
)

REQUIRED_LIFECYCLE_TRUE = (
    "createOnMount",
    "destroyOnUnmount",
    "detachCanvasOnUnmount",
    "disposeListenersOnUnmount",
)

REQUIRED_EVENTS_TRUE = ("bridgeEnabled", "unsubscribeOnUnmount")
REQUIRED_RESIZE_TRUE = ("observeContainer", "rendererResize", "respectDevicePixelRatio")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", required=True, help="Path to pixi_svelte_contract.json")
    return parser.parse_args()


def require_true(obj: dict[str, Any], key: str, bucket: list[str], ctx: str) -> None:
    if key not in obj:
        bucket.append(f"{ctx}: missing key '{key}'")
        return
    if obj[key] is not True:
        bucket.append(f"{ctx}: '{key}' must be true")


def main() -> int:
    args = parse_args()
    path = Path(args.contract)
    if not path.exists():
        print(json.dumps({"passed": False, "errors": [f"contract not found: {path}"]}))
        return 2

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(json.dumps({"passed": False, "errors": [f"invalid JSON: {exc}"]}))
        return 2

    if not isinstance(data, dict):
        print(json.dumps({"passed": False, "errors": ["contract root must be object"]}))
        return 2

    errors: list[str] = []

    for key in REQUIRED_TOP_LEVEL:
        if key not in data:
            errors.append(f"missing top-level key '{key}'")

    lifecycle = data.get("lifecycle", {})
    events = data.get("events", {})
    resize = data.get("resize", {})

    if not isinstance(lifecycle, dict):
        errors.append("lifecycle must be object")
        lifecycle = {}
    if not isinstance(events, dict):
        errors.append("events must be object")
        events = {}
    if not isinstance(resize, dict):
        errors.append("resize must be object")
        resize = {}

    for key in REQUIRED_LIFECYCLE_TRUE:
        require_true(lifecycle, key, errors, "lifecycle")
    for key in REQUIRED_EVENTS_TRUE:
        require_true(events, key, errors, "events")
    for key in REQUIRED_RESIZE_TRUE:
        require_true(resize, key, errors, "resize")

    sources = events.get("sources")
    if not isinstance(sources, list) or len(sources) == 0:
        errors.append("events: 'sources' must be a non-empty array")

    host_component = data.get("hostComponent")
    pixi_adapter = data.get("pixiAdapter")
    if isinstance(host_component, str) and not host_component.strip():
        errors.append("hostComponent must be non-empty string")
    if isinstance(pixi_adapter, str) and not pixi_adapter.strip():
        errors.append("pixiAdapter must be non-empty string")

    summary = {
        "name": data.get("name"),
        "passed": len(errors) == 0,
        "errors": errors,
    }
    print(json.dumps(summary, separators=(",", ":")))
    return 0 if summary["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
