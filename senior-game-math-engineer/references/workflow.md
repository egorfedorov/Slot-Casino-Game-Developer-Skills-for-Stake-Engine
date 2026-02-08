# Workflow

## 1. Intake

- Capture requested game modes and business constraints.
- Normalize units (bet multiplier, coin value, integer payout units).
- Record non-negotiables: max win, jurisdiction limits, feature guarantees.

## 2. Model Construction

- Build state/outcome map first, then assign probabilities/weights.
- Write EV decomposition by component:
  - Base game EV
  - Feature trigger EV
  - Bonus EV
  - Modifier EV (multipliers, expanding wilds, retriggers)
- Ensure all trigger paths terminate (no infinite loop states).

## 3. Target Mapping

- Set target bands:
  - RTP band (example: `96.00% +/- 0.20%`)
  - Hit-rate band
  - Volatility band
  - Feature entry frequency
- For multi-mode products, define each mode and blended portfolio target.

## 4. Simulation

- Run quick simulation for directional tuning (`>=1M` spins).
- Run sign-off simulation (`>=20M` spins or higher for high-volatility modes).
- Log seed, build hash/version, config snapshot, spin count, and duration.

## 5. Artifact Validation

- Validate generated book/index consistency:
  - Unique IDs
  - Positive weights
  - Weight totals sane and non-zero
  - Valid references to payout definitions
- Recompute weighted RTP from final artifacts to cross-check simulator output.

## 6. Handoff

- Produce sign-off report with:
  - Inputs and assumptions
  - Formula summary
  - Simulation summary with confidence bounds
  - Pass/fail against targets
  - Required code/data patches
  - Outstanding risks
