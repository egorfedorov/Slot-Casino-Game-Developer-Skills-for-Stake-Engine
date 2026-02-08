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

Expected row shape (aligned with Stake Engine "simulation number" and "probability" model):

- Column 0: `id` (Simulation Number) - integer-like unique identifier matching book entry
- Column 1: `weight` (Probability/Weight) - positive number determining selection frequency
- Column 2: `payoutMultiplier` (Final Payout) - numeric value matching the book entry's payout
- Column 3+: optional metadata

## Required Consistency Rules

- Every lookup ID must exist in the corresponding book file.
- Every book ID must appear in the lookup file (full coverage).
- No duplicate IDs in books or lookup tables.
- No non-positive weights.
