# Book Generation and Validation

## Inputs

- Generated book artifacts (JSONL or compressed variants).
- Lookup tables (for weighted selection if applicable).
- `index.json` metadata describing modes and outputs.

## What Must Be True

1. Every mode in the index resolves to existing files.
2. Mode metadata includes stable identity (`name` or equivalent).
3. RTP fields are present and numeric when supplied.
4. Round counts or weight totals are numeric and non-negative when supplied.

## Validation Command

```bash
node scripts/validate-books-index.mjs --index path/to/index.json --format text
```

Use `--base-dir` when index file paths are relative to another directory.

## Failure Handling

- Missing file references: fail immediately.
- No mode metadata found: fail immediately.
- RTP out of expected range: fail.
- Unknown optional fields: warn, do not fail by default.

## Reporting

Include:
- Modes checked
- Errors
- Warnings
- Final pass/fail status
