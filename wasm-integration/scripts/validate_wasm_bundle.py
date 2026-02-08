#!/usr/bin/env python3
"""Validate WASM bundle artifacts from a manifest."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


WASM_MAGIC = b"\x00asm"
WASM_V1 = b"\x01\x00\x00\x00"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, help="Path to wasm bundle manifest JSON")
    return parser.parse_args()


def load_manifest(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("manifest root must be object")
    if "modules" not in data or not isinstance(data["modules"], list) or not data["modules"]:
        raise ValueError("manifest must contain non-empty 'modules' array")
    return data


def resolve_path(root: Path, rel: str) -> Path:
    p = Path(rel)
    if p.is_absolute():
        return p
    return (root / p).resolve()


def check_wasm_binary(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        return [f"wasm file not found: {path}"]
    raw = path.read_bytes()
    if len(raw) < 8:
        return [f"wasm file too small: {path}"]
    if raw[:4] != WASM_MAGIC:
        errors.append(f"invalid wasm magic: {path}")
    if raw[4:8] != WASM_V1:
        errors.append(f"unsupported wasm version bytes: {path}")
    return errors


def contains_any(text: str, tokens: list[str]) -> bool:
    return any(token in text for token in tokens)


def validate_module(module: dict[str, Any], root: Path) -> dict[str, Any]:
    errors: list[str] = []
    required = ("name", "wasm", "loader")
    for key in required:
        if key not in module:
            errors.append(f"missing key '{key}'")
    if errors:
        return {"name": str(module.get("name", "<unknown>")), "passed": False, "errors": errors}

    name = str(module["name"])
    wasm_path = resolve_path(root, str(module["wasm"]))
    loader_path = resolve_path(root, str(module["loader"]))

    errors.extend(check_wasm_binary(wasm_path))

    if not loader_path.exists():
        errors.append(f"loader file not found: {loader_path}")
        loader_text = ""
    else:
        loader_text = loader_path.read_text(encoding="utf-8", errors="replace")
        if not contains_any(loader_text, ["WebAssembly.instantiateStreaming", "WebAssembly.instantiate"]):
            errors.append(f"loader missing WebAssembly instantiate call: {loader_path}")

    init_symbol = module.get("initSymbol")
    if init_symbol is not None and loader_text and str(init_symbol) not in loader_text:
        errors.append(f"loader missing initSymbol reference '{init_symbol}'")

    for key in ("requiredExports", "requiredImports"):
        values = module.get(key, [])
        if values is None:
            values = []
        if not isinstance(values, list):
            errors.append(f"{key} must be an array")
            continue
        for symbol in values:
            symbol_text = str(symbol)
            if loader_text and symbol_text not in loader_text:
                errors.append(f"loader missing {key} reference '{symbol_text}'")

    if bool(module.get("requiresThreads", False)) and loader_text and "SharedArrayBuffer" not in loader_text:
        errors.append("loader missing SharedArrayBuffer reference for requiresThreads=true")

    if bool(module.get("requiresSimd", False)) and loader_text and "simd" not in loader_text.lower():
        errors.append("loader missing SIMD-related reference for requiresSimd=true")

    return {
        "name": name,
        "wasmPath": str(wasm_path),
        "loaderPath": str(loader_path),
        "passed": len(errors) == 0,
        "errors": errors,
    }


def main() -> int:
    args = parse_args()
    manifest_path = Path(args.manifest)
    if not manifest_path.exists():
        print(json.dumps({"passed": False, "errors": [f"manifest not found: {manifest_path}"]}))
        return 2

    try:
        data = load_manifest(manifest_path)
    except Exception as exc:
        print(json.dumps({"passed": False, "errors": [f"invalid manifest: {exc}"]}))
        return 2

    root_value = data.get("root")
    root = manifest_path.parent if root_value is None else resolve_path(manifest_path.parent, str(root_value))

    results = []
    for module in data["modules"]:
        if not isinstance(module, dict):
            results.append({"name": "<invalid>", "passed": False, "errors": ["module entry must be object"]})
            continue
        results.append(validate_module(module, root))

    passed = all(r.get("passed", False) for r in results)
    summary = {
        "manifest": str(manifest_path.resolve()),
        "root": str(root),
        "modules": results,
        "passed": passed,
    }
    print(json.dumps(summary, separators=(",", ":")))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
