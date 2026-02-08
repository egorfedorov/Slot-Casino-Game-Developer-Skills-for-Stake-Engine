# RGS Event Contract

## Required Event Shape

Event streams must be deterministic, sequential, and frontend-consumable without recomputation.
See `https://stake-engine.com/docs/math/source-files/events` for the latest event schema.

**Standard Event Structure:**
```json
{
    "index": [int],       // Sequential ID (1, 2, 3...)
    "type": [str],        // Unique keyword (e.g., "spinStart")
    "fields": {           // Arbitrary payload
        "board": [...],
        "win": 10.0
    }
}
```

## Required Ordering

Minimum valid round pattern (State Machine alignment):
1. `Init` (optional, for state recovery)
2. `Action` (user input, e.g., spin)
3. `Reaction` (game logic, e.g., reels stop)
4. `Outcome` (result calculation)

Common event types:
- `spinStart`
- `reelsStop` (with symbol matrix)
- `winLine` (payline details)
- `bonusEnter` / `bonusExit`
- `roundResult` (terminal)

## State Machine Alignment

Ensure events map to the defined game states:
- `Idle` -> `Spinning` -> `Resolving` -> `Win/Loss` -> `Idle`
- Reference: `https://stake-engine.com/docs/math/high-level-structure/state-machine`

## Required Constraints

- First event must be `spinStart` or equivalent init event.
- Last event must be `roundResult` or equivalent terminal event.
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
