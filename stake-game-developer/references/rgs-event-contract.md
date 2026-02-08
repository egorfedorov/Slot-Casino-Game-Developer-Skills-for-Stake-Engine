# RGS Event Contract

## Required Event Shape

Event streams must be deterministic, sequential, and frontend-consumable without recomputation.

## Required Ordering

Minimum valid round pattern:

1. `spinStart`
2. `reveal` (one or more)
3. Optional interleaving:
- `winInfo`
- `multiplierUpdate`
- `bonusTrigger`
4. `roundResult` (exactly one, terminal event)

## Required Constraints

- First event must be `spinStart`.
- Last event must be `roundResult`.
- No events may appear after `roundResult`.
- `roundResult` appears once per round.
- If `basePayout`, `appliedMultiplier`, and `payout` are all present in `winInfo`, payout consistency must hold:
  - `payout ~= (basePayout * appliedMultiplier) / 100`

## Validation Command

```bash
node scripts/validate-rgs-events.mjs --input path/to/events.jsonl --format text
```

Accepted input formats:
- JSONL with one round object per line
- JSON array of events
- JSON object with `events`
- JSON object with `rounds`

## Frontend Rule

Treat the event stream as the single source of truth for displayed outcomes.
