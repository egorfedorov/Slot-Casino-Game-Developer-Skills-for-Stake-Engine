# Game Approval Checklist

Reference checklist for testing game readiness for Stake Engine.

## PreChecks

- [ ] Game authenticates with RGS successfully on game launch.
- [ ] Clicking on the bet button sends a successful play request to RGS.
- [ ] Game title is unique and does not contain terms such as Megaways, Xways.
- [ ] Game assets and imagery do not contain offensive, discriminatory, or inappropriate content.

## Game Thumbnail

- [ ] Game tile is generally bright and does not clash with the Stake Background (avoid dark edges).
- [ ] Background image is bright and appropriate for the game.
- [ ] Foreground image is appropriate, with key focus area correctly filled.
- [ ] Gradient is a similar color to the background.
- [ ] Game title fits within inner guidelines (not too close to edges).

## Math Requirements

- [ ] **RTP**: 90% -> 98%.
- [ ] **RTP Consistency**: All modes must have an RTP within 0.5% of each other (e.g., 97% game must be 96.5% - 97.5%).
- [ ] **Max Win**: Advertised max-win is achievable (hit-rate 1 in 20,000,000 or more frequent).
- [ ] **Hit Rate**: Reasonable > 0-win hit-rate (typically 3-8, not > 20 for base).

## RGS Requirements

### Bet Levels
- [ ] Respected: USD $0.10 -> $1,000 (Defaults to $1.00).
- [ ] Respected: JPY Y10 -> Y150,000 (Defaults to Y100).
- [ ] Respected: MXN MX1 -> MX15,000 (Defaults to MX10).
- [ ] **Persistence**: Refreshing game mid-spin preserves selected bet-amount (does not revert to default).

### RGS URL
- [ ] Game uses `rgs_url` query parameter to determine which server to call.
  - *Test case:* Change RGS URL query param and ensure game calls that URL.

## Frontend Requirements

### Game Rules
- [ ] Payout information per symbol is clearly communicated.
- [ ] Max multiplier and RTP displayed (clearly stated for each mode if different).
- [ ] Win combinations displayed (which lines pay, cluster sizes, scatter counts, prizes).
- [ ] Descriptions and cost for each available game mode.
- [ ] Free games trigger conditions stated (e.g., 3 Scatters = 10 spins).
- [ ] Retrigger conditions stated (e.g., 2 Scatters = +5 spins).
- [ ] **Disclaimer**: Equivalent to:
  > “Malfunction voids all pays and plays. A consistent internet connection is required. In the event of a disconnection, reload the game to finish any uncompleted bets. The expected return is calculated over many spins. Animations are not representative of any physical device, and are for illustrative purposes only. TM and © 2025 Stake Engine.”

### Responsive Checks
- [ ] Functions correctly on Desktop.
- [ ] Functions correctly on Mobile.
- [ ] Functions correctly on Popout S/M.
- [ ] **Cost Warning**: Confirmation shows when changing to bet-modes with > 2x cost (e.g., 50x bonus buy cannot be 1-click).

### Auto Play
- [ ] Confirmation step required (no 1-click auto-bet start).

### Sounds / Music
- [ ] Option in UI to disable sounds.

### Controls
- [ ] Space bar bound to bet button.

### Win Verification
- [ ] Check 10 wins for each mode against Game Rules; displayed win must match payout.

## Jurisdiction Requirements (Stake.US Social)

- [ ] Compliant with required translations for social game?
- [ ] Bet button does **not** say "Bet".
- [ ] Game Info does **not** contain restricted words.
- [ ] Bet amount field is **not** labeled "Bet Amount".
- [ ] Auto bet feature is **not** labeled "AutoBET"; popups do not contain "Bet".
- [ ] Bonus Buy label does **not** contain "BUY".
- [ ] Confirmation step does **not** include words "Buy" or "Bet".
- [ ] Insufficient funds error has **no** restricted words.
- [ ] Game supports SC (Sweepstakes Coins) and GC (Gold Coins).
- [ ] Values displayed without `$` sign prefix.
- [ ] Replay window does **not** contain restricted words.

## Replay Support

- [ ] Supports replay URLs; loads and plays desired event.
- [ ] Supports optional parameters (currency, language, amount).
- [ ] Allows replaying "event" at the end of replay.
- [ ] UI clearly displays bet cost, multiplier, and "real" bet cost (e.g., BONUS 1USD, 250USD REAL COST).

## Final Approval Checklist

- [ ] Game has bet-level templates applied (Stake US must use `us_` prefix template).
- [ ] Both Front and Math requests set as 'Approved' & ‘Active’.
- [ ] Game appeared in `stake-engine-game-approved` + `stake-engine-us-game-approved` channels.
- [ ] Approval request closed once game has rocket-ship emoji (Live on Stake).
