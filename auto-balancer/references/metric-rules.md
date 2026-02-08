# Metric Rules

## Target Metrics

Each target metric should define:

- `name`
- `target`
- `tolerance`

Acceptance rule:

- `abs(observed - target) <= tolerance`

## Hard Constraints

Each hard constraint should define:

- `name`
- `operator` (`<=`, `<`, `>=`, `>`, `==`)
- `value`

Hard constraints are blocker gates.

## Stability Rules

- Require a minimum number of runs before final pass.
- Mark non-convergence when latest runs oscillate outside tolerance.
- Keep best-run and final-run both visible in reporting.
