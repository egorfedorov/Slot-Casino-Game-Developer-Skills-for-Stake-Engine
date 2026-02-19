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
    required = ["name", "modes", "timing", "controls", "accessibility"]
    for key in required:
        if key not in spec:
            ok = error(f"Missing required field: {key}") and ok

    modes = spec.get("modes", [])
    if not isinstance(modes, list) or len(modes) == 0:
        ok = error("modes must be a non-empty array") and ok
    else:
        for idx, mode in enumerate(modes):
            if not isinstance(mode, dict):
                ok = error(f"modes[{idx}] must be an object") and ok
                continue
            for field in ["id", "label", "spinDurationMs", "settleDurationMs", "allowStop", "speedMultiplier"]:
                if field not in mode:
                    ok = error(f"modes[{idx}] missing field: {field}") and ok
            for field in ["spinDurationMs", "settleDurationMs", "speedMultiplier"]:
                val = mode.get(field)
                if isinstance(val, (int, float)) and val <= 0:
                    ok = error(f"modes[{idx}] {field} must be > 0") and ok

    timing = spec.get("timing", {})
    if isinstance(timing, dict):
        for field in ["minSpinMs", "minSettleMs", "maxTotalRoundMs"]:
            if field not in timing:
                ok = error(f"timing missing field: {field}") and ok
    else:
        ok = error("timing must be an object") and ok

    controls = spec.get("controls", {})
    if isinstance(controls, dict):
        for field in ["spinButtonStates", "speedToggleLockedStates"]:
            if field not in controls:
                ok = error(f"controls missing field: {field}") and ok
    else:
        ok = error("controls must be an object") and ok

    accessibility = spec.get("accessibility", {})
    if isinstance(accessibility, dict):
        if "reducedMotion" not in accessibility:
            ok = error("accessibility missing field: reducedMotion") and ok
    else:
        ok = error("accessibility must be an object") and ok

    max_total = timing.get("maxTotalRoundMs")
    if isinstance(max_total, (int, float)) and isinstance(modes, list):
        for idx, mode in enumerate(modes):
            spin_ms = mode.get("spinDurationMs")
            settle_ms = mode.get("settleDurationMs")
            if isinstance(spin_ms, (int, float)) and isinstance(settle_ms, (int, float)):
                if spin_ms + settle_ms > max_total:
                    ok = error(f"modes[{idx}] total duration exceeds maxTotalRoundMs") and ok

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
