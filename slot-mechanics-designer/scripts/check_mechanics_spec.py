#!/usr/bin/env python3
"""Validate slot mechanics spec integrity."""

from __future__ import annotations

import argparse
import json
from collections import deque
from pathlib import Path
from typing import Any


ALLOWED_ACTION_TYPES = {
    "award_spins",
    "set_multiplier",
    "grant_respins",
    "trigger_bonus",
    "collect_values",
    "payout",
    "transform_symbol",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Path to mechanics spec JSON file")
    return parser.parse_args()


def read_spec(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("spec root must be an object")
    return data


def as_name_set(items: list[Any], key: str) -> tuple[set[str], list[str]]:
    names: set[str] = set()
    errors: list[str] = []
    for idx, item in enumerate(items):
        if isinstance(item, str):
            name = item
        elif isinstance(item, dict) and key in item:
            name = str(item[key])
        else:
            errors.append(f"invalid entry at index {idx}")
            continue
        if name in names:
            errors.append(f"duplicate name '{name}'")
        names.add(name)
    return names, errors


def build_graph(transitions: list[dict[str, Any]]) -> dict[str, set[str]]:
    graph: dict[str, set[str]] = {}
    for t in transitions:
        src = str(t["from"])
        dst = str(t["to"])
        graph.setdefault(src, set()).add(dst)
    return graph


def reachable_states(initial_state: str, graph: dict[str, set[str]]) -> set[str]:
    visited: set[str] = set()
    queue: deque[str] = deque([initial_state])
    while queue:
        state = queue.popleft()
        if state in visited:
            continue
        visited.add(state)
        for nxt in graph.get(state, set()):
            if nxt not in visited:
                queue.append(nxt)
    return visited


def validate(data: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []

    for key in ("initialState", "states", "events", "transitions", "mechanics"):
        if key not in data:
            errors.append(f"missing top-level key '{key}'")
    if errors:
        return {"passed": False, "errors": errors}

    states = data["states"]
    events = data["events"]
    transitions = data["transitions"]
    mechanics = data["mechanics"]

    if not isinstance(states, list):
        errors.append("states must be an array")
        states = []
    if not isinstance(events, list):
        errors.append("events must be an array")
        events = []
    if not isinstance(transitions, list):
        errors.append("transitions must be an array")
        transitions = []
    if not isinstance(mechanics, list):
        errors.append("mechanics must be an array")
        mechanics = []

    state_names, state_errors = as_name_set(states, "name")
    event_names, event_errors = as_name_set(events, "name")
    errors.extend([f"states: {e}" for e in state_errors])
    errors.extend([f"events: {e}" for e in event_errors])

    initial_state = str(data["initialState"])
    if initial_state not in state_names:
        errors.append(f"initialState '{initial_state}' not found in states")

    terminal_states: set[str] = set()
    for s in states:
        if isinstance(s, dict) and bool(s.get("terminal", False)):
            terminal_states.add(str(s.get("name")))

    transition_keys: set[tuple[str, str, str]] = set()
    outgoing_count: dict[str, int] = {}
    for i, transition in enumerate(transitions):
        if not isinstance(transition, dict):
            errors.append(f"transition[{i}] must be object")
            continue
        for key in ("from", "event", "to"):
            if key not in transition:
                errors.append(f"transition[{i}] missing '{key}'")
        if any(key not in transition for key in ("from", "event", "to")):
            continue
        src = str(transition["from"])
        event = str(transition["event"])
        dst = str(transition["to"])
        if src not in state_names:
            errors.append(f"transition[{i}] unknown source state '{src}'")
        if dst not in state_names:
            errors.append(f"transition[{i}] unknown destination state '{dst}'")
        if event not in event_names:
            errors.append(f"transition[{i}] unknown event '{event}'")
        key = (src, event, dst)
        if key in transition_keys:
            errors.append(f"duplicate transition {key}")
        transition_keys.add(key)
        outgoing_count[src] = outgoing_count.get(src, 0) + 1

    graph = build_graph([t for t in transitions if isinstance(t, dict) and {"from", "to"} <= set(t.keys())])
    if initial_state in state_names:
        reachable = reachable_states(initial_state, graph)
    else:
        reachable = set()
    unreachable = sorted(state_names - reachable)
    if unreachable:
        errors.append(f"unreachable states: {unreachable}")

    for state in sorted(state_names):
        if state in terminal_states:
            continue
        if outgoing_count.get(state, 0) == 0:
            errors.append(f"non-terminal state '{state}' has no outgoing transitions")

    mechanic_ids: set[str] = set()
    for i, mechanic in enumerate(mechanics):
        if not isinstance(mechanic, dict):
            errors.append(f"mechanic[{i}] must be object")
            continue
        for key in ("id", "triggerEvent", "entryState", "targetState", "actions"):
            if key not in mechanic:
                errors.append(f"mechanic[{i}] missing '{key}'")
        if any(key not in mechanic for key in ("id", "triggerEvent", "entryState", "targetState", "actions")):
            continue

        mech_id = str(mechanic["id"])
        trigger_event = str(mechanic["triggerEvent"])
        entry_state = str(mechanic["entryState"])
        target_state = str(mechanic["targetState"])
        actions = mechanic["actions"]

        if mech_id in mechanic_ids:
            errors.append(f"duplicate mechanic id '{mech_id}'")
        mechanic_ids.add(mech_id)

        if trigger_event not in event_names:
            errors.append(f"mechanic[{i}] unknown trigger event '{trigger_event}'")
        if entry_state not in state_names:
            errors.append(f"mechanic[{i}] unknown entry state '{entry_state}'")
        if target_state not in state_names:
            errors.append(f"mechanic[{i}] unknown target state '{target_state}'")
        if (entry_state, trigger_event, target_state) not in transition_keys:
            errors.append(
                f"mechanic[{i}] has no matching transition ({entry_state}, {trigger_event}, {target_state})"
            )

        if not isinstance(actions, list) or not actions:
            errors.append(f"mechanic[{i}] actions must be non-empty array")
            continue
        for a_idx, action in enumerate(actions):
            if not isinstance(action, dict):
                errors.append(f"mechanic[{i}].actions[{a_idx}] must be object")
                continue
            if "type" not in action:
                errors.append(f"mechanic[{i}].actions[{a_idx}] missing 'type'")
                continue
            a_type = str(action["type"])
            if a_type not in ALLOWED_ACTION_TYPES:
                errors.append(
                    f"mechanic[{i}].actions[{a_idx}] unsupported type '{a_type}'"
                )

    return {
        "passed": len(errors) == 0,
        "summary": {
            "states": len(state_names),
            "events": len(event_names),
            "transitions": len(transition_keys),
            "mechanics": len(mechanic_ids),
        },
        "errors": errors,
    }


def main() -> int:
    args = parse_args()
    path = Path(args.input)
    if not path.exists():
        print(json.dumps({"passed": False, "errors": [f"input not found: {path}"]}))
        return 2

    try:
        report = validate(read_spec(path))
    except Exception as exc:
        print(json.dumps({"passed": False, "errors": [f"failed to parse/validate: {exc}"]}))
        return 2

    print(json.dumps(report, separators=(",", ":")))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
