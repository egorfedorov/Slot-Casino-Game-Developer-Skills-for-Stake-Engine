# Workflow

## 1. Scope And Mode Mapping

- Define AI features by slot mode.
- Define spin-cycle integration points for each feature.

## 2. Runtime Architecture

- Define AI systems and provider adapters.
- Define model fallback chain and safe defaults.
- Define boundaries between AI output and payout-critical logic.

## 3. Runtime Constraints

- Define latency and queue-depth limits.
- Define timeout and retry policy.
- Define deterministic fallback behavior.

## 4. Validation

- Validate mode/system/model reference integrity.
- Validate safety and telemetry coverage.

## 5. Sign-Off

- Deliver module map, budgets, and fallback behavior summary.
- Include exact implementation patch plan.
