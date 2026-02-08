# Mechanics Patterns

## Common Patterns

- Free Spins:
  - Trigger: scatter threshold
  - Actions: award spins, set starting multiplier
  - Guardrails: retrigger cap, max total spins

- Respins:
  - Trigger: symbol collection or near-miss condition
  - Actions: lock symbols, reset/extend respin counter
  - Guardrails: max respin chain length

- Collect Feature:
  - Trigger: collector + value symbol co-presence
  - Actions: aggregate values, clear/transform symbols
  - Guardrails: payout cap and clear reset condition

- Bonus Pick:
  - Trigger: bonus symbol threshold
  - Actions: enter bonus state, execute pick rounds, resolve payout
  - Guardrails: deterministic pick source and termination path

## Failure Patterns

- Mechanic references nonexistent states.
- Trigger event has no corresponding transition.
- Feature state has no exit transition.
- Retrigger logic allows unbounded loops.
- Action payload lacks required numeric values.
