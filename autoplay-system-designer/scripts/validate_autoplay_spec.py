import argparse
import json
import sys


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def error(msg):
    print(f"ERROR: {msg}")
    return False


def validate_spec(spec):
    ok = True
    required = ["name", "limits", "stopConditions", "ui", "confirmation", "accessibility"]
    for key in required:
        if key not in spec:
            ok = error(f"Missing required field: {key}") and ok

    limits = spec.get("limits", {})
    if isinstance(limits, dict):
        for field in ["maxSpins", "minSpins"]:
            if field not in limits:
                ok = error(f"limits missing field: {field}") and ok
        min_spins = limits.get("minSpins")
        max_spins = limits.get("maxSpins")
        if isinstance(min_spins, int) and isinstance(max_spins, int):
            if min_spins < 1 or max_spins < min_spins:
                ok = error("limits minSpins/maxSpins range invalid") and ok
    else:
        ok = error("limits must be an object") and ok

    stop_conditions = spec.get("stopConditions", [])
    if not isinstance(stop_conditions, list) or len(stop_conditions) == 0:
        ok = error("stopConditions must be a non-empty array") and ok

    ui = spec.get("ui", {})
    if isinstance(ui, dict):
        for field in ["spinButtonStates", "showRemainingSpins"]:
            if field not in ui:
                ok = error(f"ui missing field: {field}") and ok
    else:
        ok = error("ui must be an object") and ok

    confirmation = spec.get("confirmation", {})
    if isinstance(confirmation, dict):
        for field in ["required", "showsCost"]:
            if field not in confirmation:
                ok = error(f"confirmation missing field: {field}") and ok
        if confirmation.get("required") is not True:
            ok = error("confirmation.required must be true") and ok
    else:
        ok = error("confirmation must be an object") and ok

    accessibility = spec.get("accessibility", {})
    if isinstance(accessibility, dict):
        if "reducedMotion" not in accessibility:
            ok = error("accessibility missing field: reducedMotion") and ok
    else:
        ok = error("accessibility must be an object") and ok

    return ok


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    args = parser.parse_args()
    try:
        spec = load_json(args.input)
    except Exception as exc:
        print(f"ERROR: Failed to read input: {exc}")
        sys.exit(1)
    if not validate_spec(spec):
        sys.exit(1)
    print("OK")


if __name__ == "__main__":
    main()
