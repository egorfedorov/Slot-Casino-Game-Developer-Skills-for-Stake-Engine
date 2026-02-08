# Book Generation and Validation

## Inputs

- Generated book artifacts (JSONL or compressed variants).
- Lookup tables (for weighted selection if applicable).
- `index.json` metadata describing modes and outputs.

## Config File Contract

The `config.yml` (or `config.json`) defines the static math rules.
Reference: `https://stake-engine.com/docs/math/source-files/config`

Required fields:
- `rtp`: Target RTP percentage (e.g., 96.5).
- `volatility`: Volatility rating (Low/Medium/High).
- `paylines`: Definition of win lines (array of arrays).
- `symbols`: Symbol definitions (IDs, payouts, names).
- `reels`: Reel strip definitions (per mode if dynamic).

## Validation Rules

- **RTP Check**: `sum(weight * payout) / sum(weight)` must match `config.rtp` within tolerance.
- **Symbol Consistency**: All symbols in `events` must exist in `config.symbols`.
- **Payline Consistency**: All win lines in `events` must match `config.paylines`.

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
