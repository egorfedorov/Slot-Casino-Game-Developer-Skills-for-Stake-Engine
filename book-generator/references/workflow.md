# Workflow

## 1. Define Modes

- Enumerate modes (for example: `base`, `ante_bet`, `bonus_hunt`).
- Define per-mode cost and target distribution intent.
- Freeze event schema and required fields.

## 2. Generate Events Books

- Build `books_<mode>.jsonl` or `books_<mode>.jsonl.zst`.
- Ensure each row is valid JSON and includes stable `id`.
- Ensure required fields exist (`id`, `events`, `payoutMultiplier`).

## 3. Generate Lookup Tables

- Build `lookUpTable_<mode>_0.csv`.
- Keep IDs aligned with generated books.
- Keep weights positive and policy-compliant.

## 4. Assemble Index

- Populate `index.json` with `modes[]`:
  - `name`
  - `cost`
  - `events`
  - `weights`
- Keep paths relative to index location.

## 5. Validate Package

- Verify all files referenced in index exist.
- Verify book IDs are unique and parseable.
- Verify lookup table IDs/weights are valid and match book IDs.
- Block release on any mismatch.

## 6. Handoff

- Include generation config/version, validator output, and known caveats.
- Include file-level patch plan if any checks fail.
