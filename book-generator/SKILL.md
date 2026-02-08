---
name: book-generator
description: Generate, package, and validate weighted outcome books for slot/casino game modes. Use when defining mode book schemas, producing `books_*.jsonl(.zst)` files, generating `lookUpTable_*.csv` weights, assembling `index.json`, or running publication-ready integrity checks across books/index/weights artifacts.
---

# Book Generator

Use this skill to create deterministic book packages that backend and replay systems can consume without schema drift.

## Workflow

1. Define mode contract first.
- Specify each mode name, mode cost, event file path, and weight table path.
- Lock event schema and ID strategy before high-volume generation.

2. Generate books deterministically.
- Produce `books_<mode>.jsonl` (or `.jsonl.zst`) with stable `id` fields.
- Ensure each record has required fields (`id`, `events`, `payoutMultiplier`).
- Keep generator seeds/config versions in run logs.
21→ 3. Generate weight lookups.
22→ - Build `lookUpTable_<mode>_0.csv` with simulation ID, weight, and payout columns.
23→ - Column structure: `id` (simulation number), `weight` (probability), `payoutMultiplier`.
24→ - Keep weights positive and aligned to existing book IDs.
25→ - Normalize total weight policy per product requirements.

4. Assemble `index.json`.
- Include `modes[]` with `name`, `cost`, `events`, and `weights`.
- Verify all referenced files exist and are mode-consistent.

5. Run integrity validation before handoff.
- Validate ID uniqueness and weight coverage.
- Validate referenced files and schema-level required fields.
- Treat any missing file, duplicate ID, or ID mismatch as release blocker.

## Commands

```bash
python3 scripts/check_books_package.py \
  --index <path/to/index.json>
```

Optional quick pass:

```bash
python3 scripts/check_books_package.py \
  --index <path/to/index.json> \
  --max-rows 50000
```

## Output Contract

Return:

1. `Mode Map`: mode names, costs, and referenced files.
2. `Integrity Findings`: pass/fail by mode for books and lookup coverage.
3. `Patch Plan`: exact generator/index files to adjust.
4. `Verification`: commands and expected pass criteria.
5. `Residual Risks`: unresolved blockers.

## References

- `references/workflow.md`: step-by-step generation lifecycle.
- `references/data-contract.md`: required fields and file contracts.
- `references/signoff-template.md`: packaging and release checklist template.

## Execution Rules

- Keep IDs deterministic and stable across reruns unless version is intentionally bumped.
- Keep index references relative and artifact-local.
- Fail fast on schema/coverage mismatches instead of patching silently.
