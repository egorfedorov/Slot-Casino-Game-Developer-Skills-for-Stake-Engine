# Stake Engine Currency & Multiplier Logic

This document defines the mandatory scaling factors for all Stake Engine games. Failure to adhere to these scales will result in incorrect payouts and balance displays.

## Core Rules

There are **two distinct scaling systems** in Stake games. You must never mix them up.

| Context | Scale Factor | Usage |
| :--- | :--- | :--- |
| **API / Wallet** | `1,000,000` (1e6) | All money values sent/received from RGS (balance, bet, win). |
| **Books / Math** | `100` (1e2) | All multiplier values in `books_*.jsonl`, `lookUpTable_*.csv`, and internal math logic. |

## 1. API Scale (x1,000,000)

All monetary values exchanged with the RGS (Remote Game Server) are integers representing **micro-units**.

### Formulas
- **Read from API:** `displayAmount = apiAmount / 1_000_000`
- **Write to API:** `apiAmount = displayAmount * 1_000_000`

### Implementation Locations
- **Authentication:** `POST /wallet/authenticate` returns `balance` in micro-units.
- **Betting:** `POST /wallet/play` requires `amount` in micro-units.
- **Win/End:** `POST /wallet/end-round` requires `win` in micro-units.

### Frontend Example (TypeScript)
```typescript
// Reading balance
const balanceDisplay = formatCurrency(response.balance / 1_000_000);

// Sending bet
const betRequest = {
  amount: Math.floor(userBet * 1_000_000), // Ensure integer
  // ...
};
```

## 2. Book/Math Scale (x100)

All pre-generated outcomes (books) and probability weights use a **x100 multiplier scale** to store float multipliers as integers. This avoids floating-point issues in large datasets.

### Formulas
- **Multiplier:** `multiplierX = bookAmount / 100`
- **Win Calculation:** `winMoney = wageredBet * (bookAmount / 100)`

### Implementation Locations
- **Books (`books_*.jsonl`):** The `payoutMultiplier` field is `x100`.
  - *Example:* A `1.5x` win is stored as `150`.
- **Lookup Tables (`lookUpTable_*.csv`):** The `payoutMultiplier` column is `x100`.
- **Math SDK:** Internal win calculations (`setWin`, `finalWin`) operate on this `x100` integer scale.

### Frontend Example (TypeScript)
```typescript
// Processing a book event
const bookEvent = events[0];
const multiplier = bookEvent.payoutMultiplier / 100; // 150 -> 1.5x
const winAmount = currentBet * multiplier; 
```

## Common Pitfalls

1. **Double Scaling:** Applying `x1_000_000` to a book value.
   - *Wrong:* `win = bet * (bookValue / 1_000_000)` -> Result is 10,000x too small.
2. **Missing API Scale:** Sending raw `1.0` as bet amount.
   - *Wrong:* `amount: 1` -> RGS interprets as 0.000001 currency units.
3. **Float Drift:** Not using `Math.floor` or integer math when converting back to API format.
   - *Always* round/floor to integer before sending to RGS.

## Verification Checklist

- [ ] `Authenticate.svelte`: Balance divided by `1_000_000`.
- [ ] `rgs-requests.ts`: Bet amount multiplied by `1_000_000`.
- [ ] `amount.ts` (or similar utils): Book values divided by `100`.
- [ ] `Win.svelte`: Win display uses `bet * (bookValue / 100)`.
