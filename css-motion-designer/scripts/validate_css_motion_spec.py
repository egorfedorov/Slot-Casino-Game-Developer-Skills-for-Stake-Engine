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
    required = ["name", "placements", "recipes", "timings", "accessibility"]
    for key in required:
        if key not in spec:
            ok = error(f"Missing required field: {key}") and ok

    if "placements" in spec and not isinstance(spec["placements"], list):
        ok = error("placements must be an array") and ok

    if "recipes" in spec:
        if not isinstance(spec["recipes"], list) or len(spec["recipes"]) == 0:
            ok = error("recipes must be a non-empty array") and ok
        else:
            for idx, recipe in enumerate(spec["recipes"]):
                if not isinstance(recipe, dict):
                    ok = error(f"recipe[{idx}] must be an object") and ok
                    continue
                for field in ["id", "intent", "cssClass", "keyframes", "durationMs", "loop"]:
                    if field not in recipe:
                        ok = error(f"recipe[{idx}] missing field: {field}") and ok
                if "durationMs" in recipe and isinstance(recipe["durationMs"], (int, float)):
                    if recipe["durationMs"] <= 0:
                        ok = error(f"recipe[{idx}] durationMs must be > 0") and ok

    if "timings" in spec and isinstance(spec["timings"], dict):
        for field in ["maxDurationMs", "maxConcurrentLayers"]:
            if field not in spec["timings"]:
                ok = error(f"timings missing field: {field}") and ok
        if "maxDurationMs" in spec["timings"]:
            max_dur = spec["timings"]["maxDurationMs"]
            if isinstance(max_dur, (int, float)):
                for idx, recipe in enumerate(spec.get("recipes", [])):
                    dur = recipe.get("durationMs")
                    if isinstance(dur, (int, float)) and dur > max_dur:
                        ok = error(f"recipe[{idx}] durationMs exceeds maxDurationMs") and ok

    if "accessibility" in spec and isinstance(spec["accessibility"], dict):
        for field in ["reducedMotion", "noObstructionZones"]:
            if field not in spec["accessibility"]:
                ok = error(f"accessibility missing field: {field}") and ok
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
