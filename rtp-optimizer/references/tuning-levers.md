# Tuning Levers

## High-Impact Levers

- Paytable multipliers
- Reel-strip symbol density
- Feature trigger probability
- Bonus multiplier distribution
- Retrigger probability and cap

## Typical RTP Direction

- Increase payout values -> RTP up
- Increase dead symbols / lower feature frequency -> RTP down
- Increase bonus-entry rate -> RTP up (often volatility up)
- Cap retriggers harder -> RTP down (tail risk down)

## Safe Iteration Pattern

- Change only one major lever per iteration where possible.
- Keep a fixed spin budget for comparability.
- Use additional long-run simulations only when short-run trend is promising.

## Common Failure Patterns

- Tuning to one noisy run.
- Hiding RTP drift with volatility-only changes.
- Ignoring max-win tail behavior while chasing average RTP.
- Failing to track config hash for each run.
