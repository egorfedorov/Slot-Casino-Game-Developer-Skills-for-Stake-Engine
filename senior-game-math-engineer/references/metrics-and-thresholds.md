# Metrics And Thresholds

## Core Metrics

- `RTP = total_win / total_bet`
- `Hit Rate = winning_spins / total_spins`
- `Average Win = total_win / winning_spins`
- `Volatility Index`:
  - Prefer project-standard definition if available.
  - If absent, use coefficient of variation on non-zero wins and state this choice.
- `Feature Frequency = feature_triggers / total_spins`

## Practical Tolerances

Use explicit tolerances and report both absolute and relative deltas.

- RTP sign-off tolerance: usually `<= 0.20%` absolute from target.
- Hit-rate tolerance: usually `<= 1.00%` absolute from target.
- Volatility tolerance: define per game; do not reuse blindly across titles.
- Max win control:
  - Confirm configured max win is reachable only at intended rarity.
  - Flag if observed probability is materially above design expectation.

## Statistical Discipline

- Include confidence interval for RTP estimate.
- Do not accept final sign-off from low-sample quick runs.
- Compare at least:
  - Theoretical value from model
  - Simulated value from spin engine
  - Empirical value from generated books (weighted)

## Blocker Conditions

Treat these as release blockers:

- Simulated RTP outside sign-off tolerance.
- Max win claim inconsistent with model or simulation.
- Artifact mismatch (book/index reference errors, zero-weight pools).
- Missing reproducibility data (seed/config/version).
