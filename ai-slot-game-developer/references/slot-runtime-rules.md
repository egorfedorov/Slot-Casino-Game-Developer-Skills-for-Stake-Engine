# Slot Runtime Rules

## Critical Path Rules

- Spin resolution must complete without waiting on model response beyond configured timeout.
- Payout computation must remain deterministic and auditable.
- AI outputs may influence presentation/assist decisions but must not violate game rules.

## Mode Rules

- Each AI system must declare supported modes.
- Each mode must define fallback behavior.
- Unsupported mode invocation must fail safe.

## Safety Rules

- Require deterministic fallback for provider/model failures.
- Enforce bounded queue depth and timeout policy.
- Define explicit failure modes and mitigation behavior.

## Telemetry Rules

- Emit AI request lifecycle events.
- Emit fallback usage and latency metrics.
- Emit mode-specific outcome audit markers.
