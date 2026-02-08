# Math Game State Structure

Based on Stake Engine Architecture.

## 1. Symbol Object
Symbols are distinct class objects, not just strings.

```python
class Symbol:
    def __init__(self, config: object, name: str) -> None:
        self.name = name  # 1 or 2 letter shorthand (e.g., "H1", "W")
        self.special = False
        # Attributes determined by config.special_symbols and config.paytable
```

### Key Methods
- `assign_special_sym_function()`: Assigns behaviors (e.g., Multipliers to Wilds).
- `assign_paying_bool(config)`: Sets `is_paying` and `paytable` values.
- `check_attribute(attr)`: Returns boolean if attribute exists.
- `assign_attribute({key: value})`: Dynamically adds properties (e.g., adding a multiplier to a symbol instance).

## 2. Win Data Structure
All win methods (Lines, Ways, Cluster, Scatter) return this standardized structure.

```python
win_data = {
    'totalWin': 0.0,  # float
    'wins': [
        {
            'symbol': 'H1',
            'kind': 5,
            'win': 300,
            'positions': [{'reel': 1, 'row': 1}, ...],
            'meta': {
                'lineIndex': 12,
                'multiplier': 10,
                'winWithoutMult': 30,
                'globalMult': 1,
                'lineMultiplier': 10,
                'overlay': {'reel': 2, 'row': 2}  # Optional: Center of mass for clusters
            }
        }
    ]
}
```

## 3. Wallet Manager
Handles separation of logic, events, and wins.

- **`spin_win`**: Win for specific reveal event (reset per spin).
- **`running_bet_win`**: Cumulative win for a simulation (must match `payoutMultiplier`).
- **`basegame_wins` / `freegame_wins`**: Tracked separately for RTP analysis.

**Critical Verification:**
`self.final_win` MUST EQUAL `sum(self.basegame_wins + self.freegame_wins)`.
*Mismatch raises RuntimeError.*

## 4. Game Events
JSON objects returned from RGS. Must contain ALL display data.

**Standard Format:**
```json
{
    "index": 1,
    "type": "spinStart",
    "fields": {
        "board": [["H1", "L1"], ["L2", "H2"]],
        "balance": 100.00
    }
}
```

- **Index**: Sequential counter.
- **Type**: Unique keyword (e.g., `spinStart`, `reelStop`, `winLine`).
- **Fields**: Arbitrary data required by frontend.

**Emission:**
Events are emitted immediately after logic execution:
```python
gamestate.book.add_event(event)
```
