#!/usr/bin/env python3
"""Validate books package consistency: index, books, and lookup tables."""

from __future__ import annotations

import argparse
import csv
import io
import json
import sys
from pathlib import Path
from typing import Any, Iterable


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--index", required=True, help="Path to index.json")
    parser.add_argument(
        "--max-rows",
        type=int,
        default=0,
        help="Optional per-mode cap on book rows to read (0 = full file)",
    )
    return parser.parse_args()


def iter_lines(path: Path) -> Iterable[str]:
    if path.suffix == ".zst":
        try:
            import zstandard as zstd
        except Exception as exc:
            raise RuntimeError(f"zstd file requires zstandard package: {exc}") from exc
        with path.open("rb") as src:
            dctx = zstd.ZstdDecompressor()
            with dctx.stream_reader(src) as reader:
                wrapper = io.TextIOWrapper(reader, encoding="utf-8")
                for line in wrapper:
                    yield line
    else:
        with path.open("r", encoding="utf-8") as src:
            for line in src:
                yield line


def parse_int(value: Any, field: str) -> int:
    text = str(value).strip()
    if not text:
        raise ValueError(f"{field} is empty")
    return int(text)


def parse_float(value: Any, field: str) -> float:
    text = str(value).strip()
    if not text:
        raise ValueError(f"{field} is empty")
    return float(text)


def read_book_ids(path: Path, max_rows: int) -> tuple[set[int], int, bool, list[str]]:
    ids: set[int] = set()
    duplicates = 0
    truncated = False
    errors: list[str] = []

    for line_no, line in enumerate(iter_lines(path), start=1):
        if not line.strip():
            continue
        if max_rows > 0 and len(ids) >= max_rows:
            truncated = True
            break
        try:
            row = json.loads(line)
        except Exception as exc:
            errors.append(f"books line {line_no}: invalid JSON ({exc})")
            continue

        for key in ("id", "events", "payoutMultiplier"):
            if key not in row:
                errors.append(f"books line {line_no}: missing field '{key}'")

        if "id" not in row:
            continue
        try:
            book_id = parse_int(row["id"], "id")
        except Exception as exc:
            errors.append(f"books line {line_no}: invalid id ({exc})")
            continue

        if book_id in ids:
            duplicates += 1
        ids.add(book_id)

    if duplicates > 0:
        errors.append(f"books duplicate id count: {duplicates}")
    return ids, len(ids), truncated, errors


def read_weights(path: Path) -> tuple[set[int], int, list[str]]:
    ids: set[int] = set()
    duplicates = 0
    errors: list[str] = []

    with path.open("r", encoding="utf-8", newline="") as src:
        reader = csv.reader(src)
        for row_no, row in enumerate(reader, start=1):
            if not row:
                continue
            if row_no == 1 and row[0].strip().lower() in {"id", "book_id"}:
                continue
            if len(row) < 2:
                errors.append(f"weights row {row_no}: expected at least 2 columns")
                continue
            try:
                book_id = parse_int(row[0], "id")
                weight = parse_float(row[1], "weight")
            except Exception as exc:
                errors.append(f"weights row {row_no}: parse error ({exc})")
                continue
            if weight <= 0:
                errors.append(f"weights row {row_no}: non-positive weight {weight}")
            if book_id in ids:
                duplicates += 1
            ids.add(book_id)

    if duplicates > 0:
        errors.append(f"weights duplicate id count: {duplicates}")
    return ids, len(ids), errors


def validate_mode(index_dir: Path, mode: dict[str, Any], max_rows: int) -> dict[str, Any]:
    result: dict[str, Any] = {"name": mode.get("name", "<unknown>"), "errors": []}
    required_keys = ("name", "cost", "events", "weights")
    for key in required_keys:
        if key not in mode:
            result["errors"].append(f"mode missing key '{key}'")
    if result["errors"]:
        result["passed"] = False
        return result

    events_path = (index_dir / str(mode["events"])).resolve()
    weights_path = (index_dir / str(mode["weights"])).resolve()
    result["eventsPath"] = str(events_path)
    result["weightsPath"] = str(weights_path)

    if not events_path.exists():
        result["errors"].append(f"events file not found: {events_path}")
    if not weights_path.exists():
        result["errors"].append(f"weights file not found: {weights_path}")
    if result["errors"]:
        result["passed"] = False
        return result

    book_ids, book_count, truncated, book_errors = read_book_ids(events_path, max_rows)
    weight_ids, weight_count, weight_errors = read_weights(weights_path)
    result["bookRowsRead"] = book_count
    result["weightRowsRead"] = weight_count
    result["truncated"] = truncated
    result["errors"].extend(book_errors)
    result["errors"].extend(weight_errors)

    if truncated:
        missing_sample_ids = sorted(book_ids - weight_ids)
        if missing_sample_ids:
            result["errors"].append(
                f"lookup missing sampled book ids (showing up to 10): {missing_sample_ids[:10]}"
            )
    else:
        missing_in_weights = sorted(book_ids - weight_ids)
        missing_in_books = sorted(weight_ids - book_ids)
        if missing_in_weights:
            result["errors"].append(
                f"lookup missing book ids (showing up to 10): {missing_in_weights[:10]}"
            )
        if missing_in_books:
            result["errors"].append(
                f"lookup references unknown ids (showing up to 10): {missing_in_books[:10]}"
            )

    result["passed"] = len(result["errors"]) == 0
    return result


def main() -> int:
    args = parse_args()
    index_path = Path(args.index)
    if not index_path.exists():
        print(f"index not found: {index_path}", file=sys.stderr)
        return 2

    try:
        data = json.loads(index_path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"invalid index JSON: {exc}", file=sys.stderr)
        return 2

    modes = data.get("modes")
    if not isinstance(modes, list) or not modes:
        print("index must contain non-empty 'modes' array", file=sys.stderr)
        return 2

    mode_results = []
    for mode in modes:
        if not isinstance(mode, dict):
            mode_results.append({"name": "<invalid>", "passed": False, "errors": ["mode is not object"]})
            continue
        mode_results.append(validate_mode(index_path.parent, mode, args.max_rows))

    passed = all(m.get("passed") for m in mode_results)
    summary = {
        "index": str(index_path.resolve()),
        "modes": mode_results,
        "passed": passed,
    }
    print(json.dumps(summary, separators=(",", ":")))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
