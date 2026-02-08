# Data Contract

## index.json

Expected minimum structure:

```json
{
  "modes": [
    {
      "name": "base",
      "cost": 1,
      "events": "books_base.jsonl.zst",
      "weights": "lookUpTable_base_0.csv"
    }
  ]
}
```

## books_*.jsonl(.zst)

Expected row fields:

- `id`: integer-like unique identifier
- `events`: array of event objects
- `payoutMultiplier`: numeric value for outcome payout multiplier

## lookUpTable_*.csv

Expected row shape:

- Column 0: `id` (book ID)
- Column 1: `weight` (positive number)
- Column 2+: optional metadata (for example payout mirror values)

## Required Consistency Rules

- Every lookup ID must exist in the corresponding book file.
- Every book ID must appear in the lookup file (full coverage).
- No duplicate IDs in books or lookup tables.
- No non-positive weights.
