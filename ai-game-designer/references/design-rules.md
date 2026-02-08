# Design Rules

## Core Requirements

- Every feature must map to at least one loop.
- Every progression gate must reference an unlock condition.
- Every economy source must have balancing sink(s).

## Economy Safety

- Avoid infinite gain loops without counter-pressure.
- Keep reward curves bounded and difficulty-aware.
- Define exploit prevention rules for repeatable actions.

## Progression Safety

- Keep early progression smooth; avoid dead zones.
- Prevent contradictory unlock prerequisites.
- Define fallback recovery path for resource starvation.

## Telemetry Requirements

- Track loop completion rates.
- Track source/sink resource deltas.
- Track drop-off at progression gates.
